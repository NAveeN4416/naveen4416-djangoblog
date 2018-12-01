from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import blogdata, User_profile, Likes_dislikes,author_favorites
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db.models import Q



# Model Constants
contants = {
		'blogdata' 	     : blogdata,
		'user_profile'   : User_profile,  
		'user'		     : User,
		'likes_dislikes' : Likes_dislikes,
		'author_favorites' : author_favorites  
            } 


def table_obj(table_name,ref_id):
        if ref_id:
            obj   = contants[table_name].objects.get(id=ref_id)
        else:
            obj   = contants[table_name]()
        return obj


# Check for user login for some views
def check_login(func):
	
	def redirection(request):
		if request.user.is_authenticated:
			return True
		else:
			return False 

	def inner_func(*args,**kwargs):
		if redirection(*args,**kwargs):
			return func(*args,**kwargs)
		else:
			return redirect('login')

	return inner_func


# Create your views here.

def home(request):
	posts    = blogdata.objects.all().order_by('-id')
	
	for post in posts:
		# Count likes and dislikes of each Post
		likes 	 = Likes_dislikes.objects.filter(Q(add_id=post.id) & Q(like_status=1)).count()
		dislikes = Likes_dislikes.objects.filter(Q(add_id=post.id) & Q(like_status=0)).count()

		# Asssing counts to each post
		post.likes    = likes
		post.dislikes = dislikes

	context  = {'posts':posts}

	return render(request,'frontend/home.html',context)


def user_profile(request):

	user_id = request.user.id

	if request.is_ajax():
		if request.POST.get('user_id'):
			profile = User_profile.objects.get(user=user_id)
			user    = User.objects.get(id=user_id)

			# Save names data into Users table
			user.username   = request.POST.get('username')
			user.first_name = request.POST.get('first_name')
			user.last_name  = request.POST.get('last_name') 
			user.save()
		else:
			profile = User_profile()

		profile = User_profile.save_data(request,profile)
		return HttpResponse(profile)


	profile = User_profile.objects.filter(user=user_id)

	if(len(profile)):
		profile = profile[0]

	user    = User.objects.get(id=user_id)
	context = {'profile':profile,'user':user}
	return render(request,'frontend/user_profile.html',context)



@check_login
def add_post(request):
	if request.is_ajax():
		obj       = blogdata()
		post_data = blogdata.save_data(request,obj)
		return HttpResponse(post_data)
	return render(request,'frontend/add_post.html')


def add_details(request,ref_id=''):
	
	if ref_id!='':
		data    = blogdata.objects.get(id=ref_id)
		author  = User_profile.objects.get(user_id=data.author_id)
		
		context = dict()
		context['data']   = data
		context['author'] = author

		if request.user.is_authenticated:
			likes  = Likes_dislikes.objects.filter(Q(user_id=request.user.id) & Q(add_id=ref_id))
			if len(likes):
				likes = likes[0]
				context['likes'] = likes
		
		return render(request,'frontend/add_details.html',context)
	else:
		return redirect('frontend:home')


def likes_dislikes(request):

	table   = request.POST.get('table')
	user_id = request.user.id

	# For table Likes_dislikes
	if table == 'likes_dislikes':

		add_id  = request.POST.get('add_id')
		value   = request.POST.get('value')
		
		# Get record from database already has same record
		obj = Likes_dislikes.objects.filter(Q(user=user_id) & Q(add_id=add_id))

		if len(obj)==1:
			# Updating old Record
			obj = Likes_dislikes.objects.get(Q(user=user_id) & Q(add_id=add_id))
		else:
			# Inserting new Record 
			obj = Likes_dislikes()
		
		# Assign values to fields
		obj.user_id 	= request.user.id
		obj.add_id  	= add_id
		obj.like_status = value
		obj.save()
		return HttpResponse(obj.id)
	else:
		author_id = request.POST.get('add_id')

		obj = author_favorites()

		obj.user_id   = user_id
		obj.author_id = author_id
		obj.save()
		return HttpResponse('Yes')
