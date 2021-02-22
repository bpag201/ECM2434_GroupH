from django.shortcuts import render, get_object_or_404
from .models import User


def user_profile_self(request):
    """
    input: this page is designed to be redirected by a dash-board page, which stores the current user's login credential
    in session as 'user_login_name' (at the time I'm writing this code I assume we use the full_name in User model as
    the login name but it is obviously not appropriate)

    output: see pars
    """

    user_login_name = request.session['user_login_name']
    # we have to decide another credential for login since real name can be duplicated
    cur_user = get_object_or_404(User, full_name=user_login_name)
    pars = {
        'real_name': cur_user.full_name,
        'nick_name': cur_user.nickname,
        'email': cur_user.email,
        'college': cur_user.course.college,
        'dob': cur_user.date_of_birth,
        'resource': cur_user.resource,
        'achievement': cur_user.achievement_set.all(),
        'team': cur_user.team,  # can a user join more than one team?
        'user_tier': cur_user.user_tier.label  # maybe wrong value
    }
    return render(request, 'dummy.html', pars)  # change dummy.html to the target web page
