#!/usr/bin/python

from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    """
        To render home page
    """
    context = {}
    if request.method == "GET":
        pass
    if request.method == "POST":
        pass
    return render_to_response("base.html", context, RequestContext(request))

