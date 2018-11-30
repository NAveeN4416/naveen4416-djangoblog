from django.shortcuts import render,redirect,reverse
from .import messages as M

'''
 import these functions as 

 from core.redirections import check_auth
    


'''

## User redirections

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
        	return redirect('home:logout')
    return inner_func