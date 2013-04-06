# !/usr/bin/env python
# -*- coding: iso-8859-1 -*-

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList

class LoginForm(AuthenticationForm):
    """
    Form for logging in a user.

    Uses django's built in form for validation and other stuff.
    Only the error messages are overridden as per app's use.

    """

    # fields overridden for custom error messages
    username = forms.CharField(label=_("Username :"), max_length=30,widget=forms.TextInput(attrs={'class':'login_input'}),
            error_messages={'required': _('Username is required.')})
    password = forms.CharField(label=_("Password :"), widget=forms.PasswordInput(attrs={'class':'login_input'}),
            error_messages={'required': _('Password is required.')})

    # error_messages overridden
    error_messages = {
            'invalid_login': _("Please enter a correct username and password. "),
            'no_cookies': _("Your Web browser doesn't appear to have cookies "
                "enabled. Cookies are required for logging in."),
            'inactive': _("This account is inactive."),
            }


    def __init__(self, *args, **kwargs): # overriding for error_class
        super(LoginForm, self).__init__(error_class=NoFormClass,*args,**kwargs)

class NoFormClass(ErrorList):
    """ Class to remove class from error message rendered by forms
    Overrides ErrorList class
    """

    def __unicode__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return u''
        return ''.join([ e for e in self])
