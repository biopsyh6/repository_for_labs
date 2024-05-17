from django.contrib.auth import login as dj_login, update_session_auth_hash
from django.contrib.auth import logout as dj_logout
from django.contrib.auth import authenticate
from cinema.forms import LoginForm, UserRegistrationForm, ProfileRegistrationForm, ProfileForm
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from cinema.models import Client
import logging

logger = logging.getLogger('db_logger')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            logger.info("UserRegistrationForm and ProfileRegistrationForm are valid")
            user = user_form.save()
            profile = profile_form.save()
            user.save()
            profile.user = user
            profile.save()
            dj_login(request, user)
            logger.info("User created")
            return HttpResponseRedirect(reverse('login'))
        else:
            logger.info("UserRegistrationForm or ProfileRegistrationForm aren't valid")
            return render(request, 'cinema/account/register.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()
        return render(request, 'cinema/account/register.html', {'user_form': user_form, 'profile_form': profile_form})
    
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            logger.info("LoginForm is valid")
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    dj_login(request, user)
                    logger.info("Login user success")
                    return HttpResponseRedirect(reverse('home'))
                else:
                    return HttpResponse('Error')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'cinema/account/login.html', {'form': form})

@login_required
def logout(request):
    dj_logout(request)
    logger.info("Logout successfully")
    return HttpResponseRedirect(reverse('login'))

@login_required
def profile(request):
    user = request.user
    is_employee = False
    try:
        profile = user.client
    except:
        profile = None
    
    if profile is None:
        try:
            profile = user.employee
            is_employee = True
        except:
            profile = None
    
    if request.user.is_superuser:
        is_employee = True

    data = {'profile': profile, 'is_employee': is_employee}
    return render(request, 'cinema/account/profile.html', data)

@login_required
def edit_profile(request):
    profile = None
    if hasattr(request.user, 'client'):
        profile = request.user.client
    elif hasattr(request.user, 'employee'):
        profile = request.user.employee
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, "cinema/account/edit_profile.html", {"form": form})