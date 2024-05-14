from django.contrib.auth import login as dj_login, update_session_auth_hash
from django.contrib.auth import logout as dj_logout
from django.contrib.auth import authenticate
from cinema.forms import LoginForm, UserRegistrationForm, ProfileRegistrationForm
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from cinema.models import Client

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save()
            user.save()
            profile.user = user
            profile.save()
            dj_login(request, user)
            return HttpResponseRedirect(reverse('login'))
        else:
            return render(request, 'cinema/account/register.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()
        return render(request, 'cinema/account/register.html', {'user_form': user_form, 'profile_form': profile_form})
    
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    dj_login(request, user)
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