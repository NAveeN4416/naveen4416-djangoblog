from django.utils import timezone
from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse ,JsonResponse
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sessions.models import Session
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import EmailMessage

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils import six
from users import messages as M
from django.db.models import Q


#======================= Redirect & Auth Check methods =====================


def redirection(request):
    if request.user.is_authenticated:
        if request.user.is_staff | request.user.is_superuser:
            return True
        else:
            return False
    else:
    	return False

def check_auth(func):
    def inner_func(*args,**kwargs):
        if redirection(*args,**kwargs):
            return func(*args,**kwargs)
        else:
        	M.LOGOUT_REASON = 0 # Force logout if not admin or faculty
        	return redirect('logout')
    return inner_func


#====================================== Dashboard Views ===================================================


#@check

@check_auth
def home(request):
	return render(request,'dashboard/home.html')
























