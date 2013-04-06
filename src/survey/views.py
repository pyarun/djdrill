# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from models import Survey
from forms import SurveyForm
import logging, json

logger = logging.getLogger(__name__)

def list_survey(request):
    """
        This view list all the surveys which are currently active
    """
    slist = Survey.objects.filter(is_active=True).order_by("created_date")
    
    
    context = dict(objects=slist)
    logger.info("{user} accessed list survey page".format({"user": request.user.get_full_name()}))
    return render(request, "list_surveys.html", context )


@login_required
def create_survey(request):
    """
        Allows the logged in User to Create new Surveys.
    """
    context = {}
    if request.method == "GET":
        form = SurveyForm()
        context["form"] = form
    
    logger.info("{user} accessed create survey page".format(user=request.user.get_full_name()))
    return render(request, "create_survey.html", context)
        
        
def check_title_availability(request):
    """
        Checks if the given survey title is available to use.
        This returns a json response as:
        {status=true/false}
    """
    title = request.REQUEST.get("title")
    title_already_user = False
    if title:
        status = Survey.objects.filter(title=title).exists()
        title_already_user = not status
        
    return HttpResponse(json.dumps(dict(status=title_already_user)), content_type="application/json")
    
    