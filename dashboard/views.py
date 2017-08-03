import os

from django.shortcuts import render_to_response
from django.http import *
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test

from chat.models import Room
from .forms import URLForm, QuestionForm
from .models import PresentationURL, DarkIceRunning, ClarityRunning
from django.core.exceptions import ObjectDoesNotExist
import subprocess

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    return render_to_response('login.html', {'messagecount': getMessageCount()}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def index(request):
    query = PresentationURL.objects.filter(url__startswith='https')
    if query:
        presurl = query[0].url
    else:
        presurl = query
    if request.user.is_superuser:
        if request.POST:
            form = URLForm(request.POST)

            try:
                if form.is_valid():
                    updateURL = PresentationURL.objects.get(url__startswith='https')
                    updateURL.url = presurl = form.cleaned_data['url']
                    updateURL.save()
            except ObjectDoesNotExist:
                if form.is_valid():
                    updateURL = presurl = PresentationURL(url=form.cleaned_data['url'])
                    updateURL.save()
            return render_to_response('dashboard_professor.html', {'presurl': presurl, 'form': form, 'messagecount': getMessageCount()}, RequestContext(request))
        else:
            form = URLForm()
        return render_to_response('dashboard_professor.html', {'form': form, 'presurl': presurl, 'messagecount': getMessageCount()}, RequestContext(request))
    else:
        return render_to_response('dashboard.html', {'presurl': presurl, 'messagecount': getMessageCount()}, RequestContext(request))


@login_required(login_url='/login/')
def questions(request):
    if request.user.is_superuser:
        return render_to_response('questions_professor.html', {'messagecount': getMessageCount()}, RequestContext(request))
    else:
        form = QuestionForm()
        return render_to_response('questions.html', {'form': form, 'messagecount': getMessageCount()}, RequestContext(request))


@login_required(login_url='/login')
def audio(request):
    if request.user.is_superuser:
        return render_to_response('audioStream_professor.html', {'messagecount': getMessageCount()}, RequestContext(request))
    else:
        return render_to_response('audioStream.html', {'messagecount': getMessageCount()}, RequestContext(request))


def getMessageCount():
    room, created = Room.objects.get_or_create(label='questions')
    return room.messages.count()


@user_passes_test(lambda u: u.is_superuser)
def clarity(request):
    return render_to_response('clarity.html', {'messagecount': getMessageCount()}, RequestContext(request))

def startDarkIce(request):
    running = DarkIceRunning.objects.get_or_create().running
    if not running:
        os.system("darkice &")
        running = True
        running.save()
    return redirect(audio)

def stopDarkIce(request):
    running = DarkIceRunning.objects.get_or_create().running
    if running:
        os.system("killall darkice")
        running = False
        running.save()
    return redirect(audio)

def startClarity(request):
    running = ClarityRunning.objects.get_or_create().running
    if not running:
        subprocess.call(["python3", "/home/tyler/Documents/Classio/Classio/dashboard/micInput.py", "run"])
        running = True
        running.save()
    return redirect(clarity)

def stopClarity(request):
    running = ClarityRunning.objects.get_or_create().running
    if running:
        running = False
        running.save()
    return redirect(clarity)



# def url(request)
#     context = {
#         'request': request,
#         'url': request.url
#     }
#
#     return render_to_response('dashboard_professor.html', context=context)
