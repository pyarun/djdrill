#!/usr/bin/python

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from forms import LoginForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import views as auth_views

def home(request):
    """
        To render home page
    """
    context = {}
    if request.method == "GET":
        pass
    if request.method == "POST":
        pass
    return render_to_response("index.html", context, RequestContext(request))

@csrf_protect
def login(request):
    """ Function to log user in """
    context = {}
    if request.method == 'GET':
        form = LoginForm()
        context['form'] = form

    if request.method == 'POST':

        redirect_to = request.POST.get('next', '')
        auth_response = auth_views.login(request, authentication_form=LoginForm)

        # if response is http response redirect then flag success
        if type(auth_response) == HttpResponseRedirect:
            context['redirect_to'] = redirect_to
            context['success'] = True
            return HttpResponseRedirect(reverse('home'))
        else:
            context.update(auth_response.context_data)  # update login context
    return render_to_response("login.html", context, RequestContext(request))

def logout(request):
    """
        logout
    """
    auth_logout(request)
    return HttpResponseRedirect(reverse('home'))
