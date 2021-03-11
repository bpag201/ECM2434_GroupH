from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from .utils import *
from .forms import *
from .api import *
import json
from random import sample


def register_view(request):
    if not request.user.is_anonymous:
        return redirect('navigation')
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
            request.session.set_expiry(18000)
            return redirect('navigation')
        else:
            return render(request, "register.html", {'form': form})
    else:
        form = RegisterForm()
    return render(request, "register.html", {'form': form})


def login_view(request):
    if not request.user.is_anonymous:
        return redirect('navigation')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('paswd')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session.set_expiry(18000)
                return redirect('navigation')
            else:
                form.errors.important = unpw_errmsg_mismatch
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def home_view(request):
    if not request.user.is_anonymous:
        return redirect('navigation')
    return render(request, "homepage.html")


def navigation_view(request):
    if not request.user.is_anonymous:
        return render(request, 'navigation.html')
    else:
        return redirect('home')


def profile_view(request, username):
    if not request.user.is_anonymous:
        if request.method == 'POST':
            form = request.POST
            cur_user = request.user
            cur_user_profile = cur_user.profile
            last_name = form.get('last-name', None)
            first_name = form.get('first-name', None)
            avatar = request.FILES.get('avatar')
            title = form.get('titles')
            nickname = form.get('nickname', None)
            date_of_birth = form.get('DOB', None)
            email = form.get('email')
            course = form.get('course', None)
            team_name = form.get('team', None)
            society = form.get('society')

            if last_name != '':
                cur_user.last_name = last_name
            if first_name != '':
                cur_user.first_name = first_name
            if avatar is not None:
                if avatar.name.endswith(('jpg', 'png', 'JPG', 'PNG')):
                    cur_user_profile.avatar = avatar
            if title != '':
                cur_user_profile.title = title
            if nickname != '':
                cur_user_profile.nickname = nickname
            if date_of_birth != '':
                cur_user_profile.dob = date_of_birth
            if course != '':
                cur_user_profile.course = course
            if email != '':
                cur_user.email = email
            if team_name != '':
                cur_user_profile.team = team_name
            if society != '':
                cur_user_profile.society = society
            cur_user.save()
            cur_user_profile.save()
        try:
            user = User.objects.get(username=username)
            profile = user.profile

            is_self = user.username == request.user.username
            try:
                user_avatar = profile.avatar.url
            except Exception:
                user_avatar = "images/bex3.jpg"

            user_items = list(profile.item_set.all())
            inventory = []
            for i in user_items:
                inventory.append([i.item_name, get_loot_detail(i.item_name)[0], get_loot_detail(i.item_name)[1]])

            user_rank = get_user_rank(profile.score)
            args = {"user_full_name": "{} {}".format(user.first_name, user.last_name),
                    "DOB": profile.dob,
                    "avatar": user_avatar,
                    "user_nickname": profile.nickname,
                    "email": user.email,
                    "gold": profile.gold,
                    "course": profile.course,
                    "team": profile.team,
                    "society": profile.society,
                    "rank": user_rank,
                    "is_self": is_self,
                    "inventory": inventory,
                    "title": profile.title,
                    }
            return render(request, "profile.html", args)
        except ObjectDoesNotExist:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        except MultipleObjectsReturned:
            return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        return redirect('home')


def shop(request):
    if not request.user.is_anonymous:
        if request.method == 'POST':
            updates = json.loads(request.body)
            if "resource" in updates:
                request.user.profile.gold = updates["resource"]
                request.user.profile.save()
            if "new_item" in updates:
                target_item, created = Item.objects.get_or_create(
                    item_name=updates["new_item"],
                    item_owner=request.user.profile
                )
                if not created:
                    target_item.item_amount += 1
                target_item.save()
        shop_items = []
        for i in range(0, 2):
            shop_items.append(allocate_loot())
        args = {
            "shop_items": shop_items,
            "gold": request.user.profile.gold
        }
        return render(request, 'shop.html', args)
    else:
        return redirect('home')


def answer_quiz(request):
    if not request.user.is_anonymous:
        form = request.POST
        try:
            target_coll = get_object_or_404(Collection, coll_id=form.get('i', None))
            quiz_cards = target_coll.coll_cards.filter(card_type=1)
            if len(quiz_cards) == 0:
                return redirect('card_set_list', invalid=1)
            elif len(quiz_cards) < 5:
                selected_questions = quiz_cards
            else:
                selected_questions = sample(list(quiz_cards), 5)
        except Exception:
            return redirect('card_set_list', invalid=2)

        pars = {
            "questions": selected_questions,
            "question_num": len(selected_questions),
            "i": form.get('i', None),
        }
        return render(request, 'answer_quiz.html', pars)

    else:
        return redirect('home')


def result(request):
    if not request.user.is_anonymous:
        cur_user = request.user
        if request.method == 'POST':
            form = request.POST
            question_num = form.get('question_num', 0)
            quiz_result = []
            mark = 0
            for i in range(1, int(question_num) + 1):
                answer_index = "answer" + str(i)
                selected = form.get(answer_index, None)
                try:
                    selected_option = get_object_or_404(Option, opt_id=uuid.UUID(selected))
                    if selected_option.opt_isCorrect:
                        mark += 1  # rewards are depend on marks
                    correct_option = selected_option.opt_cid.option_set.get(opt_isCorrect=True)
                    quiz_result.append([selected_option.opt_content, correct_option.opt_content])
                except Exception:
                    pass
            pars = {
                "ques_amount": question_num,
                "quiz_result": quiz_result,
                "i": form.get('i', None),
                "score_added": mark,
                "gold_added": mark * 5,
            }

            cur_user. profile.score += mark
            cur_user.profile.gold += mark * 5
            cur_user.profile.save()

            return render(request, 'result.html', pars)
    else:
        return redirect('home')


def flash_card(request):  # redirect output: index
    if not request.user.is_anonymous:
        cur_user = request.user
        if request.method == 'POST':
            form = request.POST
            target_card = None
            for c in Card.objects.all():
                if str(c.card_id) == form.get('current_card'):
                    target_card = c.card_id
            try:
                new_comt = Comment(comt_user=cur_user, comt_type='C', comt_content=form.get('content', ""),
                                   comt_father_id=form.get('i'),
                                   comt_card=Card.objects.get(card_id=target_card))
                new_comt.save()
            except Exception:
                pass
        else:
            form = request.GET
        try:
            target_collection = get_object_or_404(Collection, coll_id=form.get('i', None))
        except Exception:
            return redirect('card_set_list', invalid=2)
        cards = get_all_cards(target_collection)
        questions = []
        answers = []
        comments = []
        card_ids = []
        for card in cards:
            question = card.card_content
            questions.append(question)
            answer = card.option_set.get(opt_isCorrect=True).opt_content
            answers.append(answer)
            # comment_raw = get_all_comt(card)
            comment = [[x.comt_user.profile.nickname, x.comt_content] for x in card.comment_set.all()]
            comments.append(comment)
            card_ids.append(str(card.card_id))
        pars = {
            "questions": questions,
            "answers": answers,
            "comments": comments,
            "i": form.get('i', None),
            "card_ids": card_ids,
        }
        return render(request, 'flash_card.html', pars)
    else:
        return redirect('home')


def card_set_list(request, invalid=0):
    if not request.user.is_anonymous:
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
            all_sets = Collection.objects.all()
            pg_num = int(request.GET.get("pg_num", 1))
        pars = paging(all_sets)
        pg_obj = get_page(pg_num, pars)
        output = {
            "card_sets": pg_obj,
            "pg_size": len(pars),
            "cur_page": pg_num,
            "search_tags": json.dumps(tags),
            "invalid_quiz": invalid,
        }
        return render(request, 'card_sets.html', output)
    else:
        return redirect('home')


def view_set(request, invalid=0):
    if not request.user.is_anonymous:
        cur_user = request.user
        if request.method == 'POST':
            form = request.POST
            source = form.get('source', None)
            if source == 'delete':  # when deleting a set
                coll_id = form.get('del_id', None)
                try:
                    dlt_coll = get_object_or_404(Collection, coll_id=coll_id)
                except Exception:
                    return redirect('view_set', invalid=1)
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
        my_sets = list(Collection.objects.filter(coll_creator=cur_user))
        pars = {"my_sets": my_sets, "invalid": invalid}
        return render(request, 'view_set.html', pars)
    else:
        return redirect('home')


def edit_set(request):
    if not request.user.is_anonymous:
        cur_user = request.user
        form = None
        err_msg = 'null'
        if request.method == 'GET':
            form = request.GET
        elif request.method == 'POST':
            form = request.POST
            source = form.get('source', None)
            if source == 'delete_card':  # when deleting a card
                dlt_id = form.get('dlt_id', None)
                try:
                    dlt_card = get_object_or_404(Card, card_id=dlt_id)
                    dlt_card.delete()
                except Exception:
                    pass
            elif source == 'add_card':
                try:
                    target_coll = get_object_or_404(Collection, coll_id=form.get('coll_id', None))
                    new_card = Card(card_content=form.get('question'), card_type=form.get('isMultipleChoice', 0),
                                    card_creator=cur_user)
                    correct_option = Option(opt_cid=new_card, opt_content=form.get('correct_answer'),
                                            opt_isCorrect=True)
                    alt1 = Option(opt_cid=new_card, opt_content=form.get('alternative1'))
                    alt2 = Option(opt_cid=new_card, opt_content=form.get('alternative2'))
                    alt3 = Option(opt_cid=new_card, opt_content=form.get('alternative3'))
                    if form.get('isMultipleChoice', 0) != 0 and (correct_option.opt_content in [alt3.opt_content,
                                                    alt2.opt_content, alt1.opt_content] or alt1.opt_content in [alt2.opt_content,
                                                    alt3.opt_content] or alt2.opt_content == alt3.opt_content):
                        print(form.get('isMultipleChoice'))
                        err_msg = "You cannot set the same content to different options!"
                    else:
                        new_card.save()
                        correct_option.save()
                        alt1.save()
                        alt2.save()
                        alt3.save()
                        target_coll.coll_cards.add(new_card)  # bugs exist in api.py so use this statement instead
                except Exception:
                    pass

        coll_id = form.get('coll_id', None)
        if coll_id is None:
            return HttpResponse("Haven't  found this card set, please try another one.")
        try:
            target_coll = get_object_or_404(Collection, coll_id=coll_id)
        except Exception:
            return redirect('view_set')
        target_cards_raw = get_all_cards(target_coll)
        # divide list into chunks of size 4, in order to display them properly
        target_cards = []
        for i in range(0, len(target_cards_raw), 4):
            target_cards.append(target_cards_raw[i:i + 4])
        pars = {"target_cards": target_cards, "err_msg": err_msg, "coll_id": form.get('coll_id')}
        return render(request, 'edit_set.html', pars)
    else:
        return redirect('home')


def log_out_operation(request):
    logout(request)
    return redirect('home')


def leaderboard(request):
    if request.user.is_anonymous:
        return redirect('home')
    top_players = Profile.objects.all().order_by('-score')[:15]
    pars = {"top_players": top_players}
    return render(request, 'leaderboard.html', pars)
