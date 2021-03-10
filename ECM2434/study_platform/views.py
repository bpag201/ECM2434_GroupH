from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError, transaction
from guardian.shortcuts import assign_perm
from .utils import paging, get_page
from .forms import *
from .api import *
import json
from random import sample


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            fstname = form.cleaned_data['fstname']
            sndname = form.cleaned_data['sndname']
            paswd = form.cleaned_data['paswd1']
            email = form.cleaned_data['email']

            u = User.objects.create(username=username, first_name=fstname, last_name=sndname, email=email)
            u.set_password(raw_password=paswd)
            u.save()

            p = Profile(user=u)
            p.save()

            login(request, u)

            assign_perm('change_profile', u, p)
            return redirect("/profile/"+username)
        else:
            return render(request, "register.html", {'form': form})
    else:
        form = RegisterForm()
    return render(request, "register.html", {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('paswd')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/profile/"+username)
            else:
                form.errors.important = unpw_errmsg_mismatch
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def home_view(request):
    return render(request, "homepage.html")


def navigation_view(request):
    return render(request, 'navigation.html')


def profile_view(request, username):
    try:
        target = User.objects.filter(username=username)[0]
        profile = get_profile(target)

        args = {"user_full_name": "{} {}".format(target.first_name, target.last_name),
                "DOB": profile.dob,
                "user_nickname": profile.nickname,
                "email": target.email,
                "gold": profile.gold,
                "perm_valid": request.user.has_perm("change_profile", profile)
                }
        return render(request, "profile.html", args)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    except MultipleObjectsReturned:
        return HttpResponseNotFound('<h1>Page not found</h1>')


""" the following pages are solely web pages which has no communication with the database yet, but only skeletons
    which describes what the corresponding functions should look like. """


def shop(request):
    return render(request, 'shop.html')


def answer_quiz(request):
    if request.session.get('username', None) is not None:
        form = request.POST
        target_coll = get_object_or_404(Collection, coll_id=form.get('i', None))
        quiz_cards = target_coll.coll_cards.filter(card_type=1)
        if len(quiz_cards) == 0:
            pass  # TODO: return an error page
        elif len(quiz_cards) < 5:
            selected_questions = quiz_cards
        else:
            selected_questions = sample(quiz_cards, 5)
        pars = {
            "questions": selected_questions,
            "question_num": len(selected_questions),
            "i": form.get('i', None),
        }
        return render(request, 'answer_quiz.html', pars)

    else:
        return redirect('groupH:home')


def result(request):
    if request.session.get('username', None) is not None:
        cur_user = get_object_or_404(User, username=request.session.get('username'))
        if request.method == 'POST':
            form = request.POST
            question_num = form.get('question_num', 0)
            quiz_result = []
            mark = 0
            for i in range(1, int(question_num) + 1):
                answer_index = "answer" + str(i)
                selected = form.get(answer_index, None)
                selected_option = get_object_or_404(Option, opt_id=uuid.UUID(selected))
                if selected_option.opt_isCorrect:
                    mark += 1  # rewards are depend on marks
                correct_option = selected_option.opt_cid.option_set.get(opt_isCorrect=True)
                quiz_result.append([selected_option.opt_content, correct_option.opt_content])
            pars = {
                "ques_amount": question_num,
                "quiz_result": quiz_result,
                "i": form.get('i', None),
            }

            cur_user.userprofile.score += mark
            cur_user.userprofile.resource += mark * 5
            cur_user.userprofile.save()

            return render(request, 'result.html', pars)
    else:
        return redirect('groupH:home')


def flash_card(request):  # redirect output: index
    if request.session.get('username', None) is not None:
        cur_user = get_object_or_404(User, username=request.session.get('username'))
        if request.method == 'POST':
            form = request.POST
            new_comt = Comment(comt_user=cur_user, comt_type='C', comt_content=form.get('content', ""), comt_like=0)
            new_comt.save()
            # TODO: This feature is not done since comments are not point to a specific card.
        else:
            form = request.GET
        target_collection = get_object_or_404(Collection, coll_id=form.get('i', None))
        cards = get_all_cards(target_collection)
        questions = []
        answers = []
        comments = []
        for card in cards:
            question = card.card_content
            questions.append(question)
            answer = card.option_set.get(opt_isCorrect=True).opt_content
            answers.append(answer)
            comment_raw = get_all_comt(card)
            comment = [[x.comt_user.userprofile.nickname, x.comt_content] for x in comment_raw]
            comments.append(comment)
        pars = {
            "questions": questions,
            "answers": answers,
            "comments": comments,
            "i": form.get('i', None),
        }
        return render(request, 'flash_card.html', pars)
    else:
        return redirect('groupH:home')


""" In order to implement pagination on the web page, several testing data is added to this function """


def card_set_list(request):
    if request.session.get('username', None) is not None:
        all_sets = Collection
        tags = []
        pg_num = 0
        if request.method == 'POST':
            # get tags, find collections by tags
            form = request.POST
            tags = form.get('input', "")
            tags = tags.split(",")
            all_sets = list(Collection.objects.filter(coll_tags__name__in=tags).distinct())
            pg_num = int(form.get("pg_num", 1))
        elif request.method == 'GET':
            all_sets = Collection.objects.all()  # TODO:Check if this syntax is correct
            pg_num = int(request.GET.get("pg_num", 1))
        pars = paging(all_sets)
        pg_obj = get_page(pg_num, pars)
        output = {
            "card_sets": pg_obj,
            "pg_size": len(pars),
            "cur_page": pg_num,
            "search_tags": json.dumps(tags),
        }
        return render(request, 'card_sets.html', output)
    else:
        return redirect('groupH:home')


def view_set(request):
    if request.session.get('username', None) is not None:
        cur_user = get_object_or_404(User, username=request.session.get('username'))
        if request.method == 'POST':
            form = request.POST
            source = form.get('source', None)
            if source == 'delete':  # when deleting a set
                coll_id = form.get('del_id', None)
                dlt_coll = get_object_or_404(Collection, coll_id=coll_id)
                dlt_coll.delete()
            elif source == 'add':
                new_set = Collection(coll_title=form.get('coll_title'),
                                     coll_description=form.get('coll_description', None),
                                     coll_creator=cur_user)
                form_tags = form.get('tags', None)
                form_tags = form_tags.split(',')
                # add_tags_to_coll(new_set, form_tags)
                for form_tag in form_tags:
                    new_set.coll_tags.add(form_tag)
                new_set.save()
                # TODO: Note that some field is not nullable, need to apply bootstrap validation
        my_sets = list(Collection.objects.filter(coll_creator=cur_user))
        pars = {"my_sets": my_sets}
        return render(request, 'view_set.html', pars)
    else:
        return redirect('groupH:home')


def edit_set(request):
    if request.session.get('username', None) is not None:
        cur_user = get_object_or_404(User, username=request.session.get('username'))
        form = None
        err_msg = None
        if request.method == 'GET':
            form = request.GET
        elif request.method == 'POST':
            form = request.POST
            source = form.get('source', None)
            if source == 'delete_card':  # when deleting a card
                dlt_id = form.get('dlt_id', None)
                dlt_card = get_object_or_404(Card, card_id=dlt_id)
                dlt_card.delete()
            elif source == 'add_card':
                # TODO:instead of using default value, it's better to use bootstrap validation here
                target_coll = get_object_or_404(Collection, coll_id=form.get('coll_id', None))
                new_card = Card(card_content=form.get('question'), card_type=form.get('isMultipleChoice', 0),
                                card_creator=cur_user)
                correct_option = Option(opt_cid=new_card, opt_content=form.get('correct_answer'),
                                        opt_isCorrect=True)
                alt1 = Option(opt_cid=new_card, opt_content=form.get('alternative1'))
                alt2 = Option(opt_cid=new_card, opt_content=form.get('alternative2'))
                alt3 = Option(opt_cid=new_card, opt_content=form.get('alternative3'))
                if correct_option in [alt3, alt2, alt1] or alt1 in [alt2, alt3] or alt2 == alt3:
                    err_msg = "You can't set the same content to different options!"
                else:
                    new_card.save()
                    correct_option.save()
                    alt1.save()
                    alt2.save()
                    alt3.save()
                    add_card2coll(new_card, target_coll)

        coll_id = form.get('coll_id', None)
        if coll_id is None:
            return HttpResponse("Haven't  found this card set, please try another one.")
        target_coll = get_object_or_404(Collection, coll_id=coll_id)
        target_cards_raw = get_all_cards(target_coll)
        # divide list into chunks of size 4, in order to display them properly
        target_cards = []
        for i in range(0, len(target_cards_raw), 4):
            target_cards.append(target_cards_raw[i:i + 4])
        pars = {"target_cards": target_cards, "err_msg": err_msg, "coll_id": form.get('coll_id')}
        return render(request, 'edit_set.html', pars)
    else:
        return redirect('groupH:home')
