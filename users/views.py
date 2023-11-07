from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Profile, Skill, Message
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import customusercreationform, profileform, skillform, messageform
from django.db.models import Q
from .utils import searchprofiles, paginateprofiles


# Create your views here.

def loginuser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'username not exist')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'username or password incorrect')

    return render(request, 'users/login_register.html')


def logoutuser(request):
    logout(request)
    messages.error(request, 'user logged out')
    return redirect('login')


def registeruser(request):
    page = 'register'
    form = customusercreationform()
    if request.method == 'POST':
        form = customusercreationform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'user account created')

            login(request, user)
            return redirect('edit-account')
        else:
            messages.success(request, 'error in registeration ')
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles, search_query = searchprofiles(request)
    custom_range, profiles = paginateprofiles(request, profiles, 3)
    context = {
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range
    }
    return render(request, 'users/profiles.html', context)


def userprofile(request, pk):
    profile = Profile.objects.get(id=pk)
    topskills = profile.skill_set.exclude(description__exact="")
    otherskills = profile.skill_set.filter(description="")

    context = {
        'profile': profile,
        'topskills': topskills,
        'otherskills': otherskills,
    }
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def useraccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editaccount(request):
    profile = request.user.profile
    form = profileform(instance=profile)
    if request.method == 'POST':
        form = profileform(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createskill(request):
    profile = request.user.profile
    form = skillform()
    if request.method == 'POST':
        form = skillform(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'skill added successfully')
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateskill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = skillform(instance=skill)
    if request.method == 'POST':
        form = skillform(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'skill updated successfully')
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteskill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'skill deleted successfully')
        return redirect('account')
    context = {'object': skill}
    return render(request, 'delete-object.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messagerequests = profile.messages.all()
    unreadcount = messagerequests.filter(is_read=False).count()
    context = {
        'messagerequests': messagerequests,
        'unreadcount': unreadcount
    }
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewmessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def createmessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = messageform()
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = messageform(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                sender.email = sender.email
            message.save()

            messages.success(request, 'your message successfully sent')
            return redirect('user-profile', pk=recipient.id)
    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)
