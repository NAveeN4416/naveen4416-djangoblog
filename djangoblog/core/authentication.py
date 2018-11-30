from django.utils import timezone
from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse ,JsonResponse
from core.auth_forms import SignUpForm
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

####

from django.utils import six
from core import messages as M


'''
  import these classes as 

# For Password and Account Verification
  from core.authentication import Secure as secure
  

# For Authentication
  from core.authentication import  Authentication as authviews
  urlpatterns  = [
                    url(r'^signup/', authviews.signup,name='signup'),
                    url(r'^login/' , authviews.login,name='login'),
                    url(r'^logout/', authviews.logout,name='logout'),
                  ]
'''


class TokenGenerator(PasswordResetTokenGenerator):

  def _make_hash_value(self, user, timestamp):
    return (
            	six.text_type(user.pk) + six.text_type(timestamp) +
            	six.text_type(user.username)  )


account_activation_token = TokenGenerator()

'''================================================================================='''

class Authentication:

  def signup(request):
    if request.method=='POST':
      form = SignUpForm(request.POST)
      if form.is_valid():
        form.save()
        username     = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user         = authenticate(username=username,password=raw_password)
        user.is_active = False
        user.save()

        if user is not None and user is not 0:
          if user.is_active:
            auth_login(request, user)
            return redirect('home:index')
          else:
            messages.error(request,'Verify Email To Login')
            Secure.send_email_verification(request,user.pk,'activate')
        elif user is 0:
          messages.error(request,M.MESSAGES[5])
        else:
          messages.error(request,'username or password is incorrect')
        return redirect('home:indexlogin')
      else:
        return render(request,'registration/register.html',{'form':form})      
    else:
      form = SignUpForm()
      return render(request,'registration/register.html',{'form':form})      


  def login(request):

    if request.method == 'POST':    # Checks request is from login form or not

      form         = AuthenticationForm(request.POST)
      username     = request.POST['username']
      raw_password = request.POST['password']
      user = authenticate(username=username, password=raw_password)

      if user is not None and user is not 0:
        if user.is_active:
          auth_login(request, user)
        else:
          messages.info(request,M.MESSAGES[2])
      elif user is 0:
        messages.info(request,M.MESSAGES[5])
      else:
        messages.info(request,M.MESSAGES[4])
      return redirect('home:login')

    else: # in user presence redirect otherwise show login form 

      if request.user.is_authenticated:
        if request.user.is_staff | request.user.is_superuser:
          return redirect('home:index')
        else:
          return redirect('frontend:index')
      else:
        form = AuthenticationForm()
        return render(request,'registration/login.html',{'form':form})


  def logout(request,reason=''):
    if request.user.is_authenticated:
      user_id = request.user.pk
      unexpired_sessions = Session.objects.filter(expire_date__gte=timezone.now())
      [
          session.delete() for session in unexpired_sessions
          if str(user_id) == session.get_decoded().get('_auth_user_id')
      ]
      logout_reason(request)
    return redirect('login')

# Functions

def authenticate(username, password):
      #Check For User Existance
  try:
    user        = User.objects.get(username=username)
    pwd_valid   = check_password(password, user.password)

    if pwd_valid:
      user = User.objects.get(username=username)
      return user
    return None
  except User.DoesNotExist:
    return 0

def logout_reason(request):
    if M.LOGOUT_REASON:
      messages.error(request,M.MESSAGES[M.LOGOUT_REASON])
    else:
      messages.error(request,M.MESSAGES[M.LOGOUT_REASON])
    M.LOGOUT_REASON = 1

'''======================================================================================'''

class Secure:

  def __init__(self):
    pass

  def send_email_verification(request,user_id,path):

    user         = User.objects.get(pk=user_id)
    current_site = get_current_site(request)
    mail_subject = 'Activate Your Django Account'
    context      = {
                      'user'  : user.username,
                      'domain': current_site.domain,
                      'uid'   : urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                      'token' : account_activation_token.make_token(user),
                      'path'  : path,
                    }
    message      = render_to_string('registration/verify_email.html', context)
    to_email     = user.email
    email        = EmailMessage(mail_subject, message, to=[to_email])

    if email.send():
      return 1
    else:
      return 0

  def verify_email(uidb64, token):
    try:
      uid  = urlsafe_base64_decode(uidb64).decode()
      user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
      user = None

    if user is not None and account_activation_token.check_token(user, token):
      user.is_active = True
      user.save()
      if user.is_active:
        return user
      else:
        return 0
    else:
      return 1

  def password_changed(request,user):
    Subject = 'Subject'
    Body    = render_to_string('registration/chang_pass_success.html',{'user':user})
    email   = EmailMessage(Subject, Body, to=[user.email])
    if email.send():
      return 1
    else:
      return 0


'''=================================================='''

