from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
import os
from os.path import join
from django.conf import settings
 
# Create your models here.

class blogdata(models.Model):
	author = models.ForeignKey(User,on_delete=models.CASCADE)
	title  = models.CharField(max_length=500)
	data   = models.CharField(max_length=5000)
	posted_date   = models.DateTimeField(default=datetime.now(), blank=True)

	def __str__(self):
		return '{}'.format(self.title)

	def save_data(request,obj):
		obj.author_id = request.user.id
		obj.title     = request.POST['title'] 
		obj.data      = request.POST['data'] 
		
		if(obj.save()):
			return obj
		else:
			return None


class User_profile(models.Model):

	user  = models.ForeignKey(User,on_delete=models.CASCADE)
	image = models.FileField(upload_to='user_profilepics')
	created_at	= models.DateTimeField(default=datetime.now(), blank=True)


	def  __str__(self):
		return '{}'.format(self.user)

	def save_data(request,obj):
		obj.user_id = request.user.id
			
		old_image = request.POST.get('old_image')
		new_image = request.FILES.get('image')

		if new_image:
			obj.image = new_image
			if old_image:
				pass
				os.remove(os.path.join(settings.MEDIA_ROOT, old_image))
		else:
			obj.image = old_image
			

		if(obj.save()):
			return obj
		else:
			return None


class Likes_dislikes(models.Model):
	user   = models.ForeignKey(User,on_delete=models.CASCADE)
	add    = models.ForeignKey(blogdata,on_delete=models.CASCADE)
	like_status = models.BooleanField(default=True)


	def  __str__(self):
		return '{}-{}-{}'.format(self.user,self.add,self.like_status)


class author_favorites(models.Model):
	user_id   = models.IntegerField()
	author = models.ForeignKey(User,on_delete=models.CASCADE)


	def __str__(self):
		return '{}-{}'.format(self.user,self.author)