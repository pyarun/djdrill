'''
Created on 06-Apr-2013

@author: arun
'''
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template


urlpatterns = patterns("survey",
        
        url("list$", "views.list_survey", name="list_survey"),
        url("new$", "views.create_survey", name="create_survey"),
        
        url("check/title/availablity$", "views.check_title_availability", name="check_title_availability"),
                       


) 