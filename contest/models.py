from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import os, shutil, errno
from django.contrib.auth.models import Permission, User


# Create your models here.
class team(models.Model):
	teamId = models.CharField(max_length=200, unique = True)
	password = models.CharField(max_length=30)

	REQUIRED_FIELDS = ('teamId','password',)
	USERNAME_FIELD = ('teamId',)


class question(models.Model):
	statement = models.CharField(max_length=5000, unique = True)

class timeRemaining(models.Model):
	user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
	time = models.IntegerField()
	completion = models.BooleanField(default=False)

class submission(models.Model):
	user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
	question1 = models.CharField(max_length=50, null=True)
	question2 = models.CharField(max_length=50, null=True)
	question3 = models.CharField(max_length=50, null=True)
	question4 = models.CharField(max_length=50, null=True)
	question5 = models.CharField(max_length=50, null=True)
	penalty = models.IntegerField(null=True, default=0)
	marks = models.IntegerField(default=0)
	time = models.CharField(max_length=20, default=0)



@receiver(post_save, sender=question)
def question_inserted(sender, instance, created, **kwargs):
	static_dir = 'contest/static/questions'
	new_dir = 'question'+str(instance.id)
	new_dir_path = os.path.join(static_dir, new_dir)
	try:
		os.mkdir(new_dir_path)
	except OSError as e:
		if e.errno != errno.EEXIST:
			pass
		else:
			print(e)

@receiver(post_delete, sender=question)
def question_deleted(sender, instance, **kwargs):
	static_dir = 'contest/static/questions'
	new_dir = 'question'+str(instance.id)
	new_dir_path = os.path.join(static_dir, new_dir)
	try:
		shutil.rmtree(new_dir_path)
	except OSError:
		print(e)

@receiver(post_delete, sender=User)
def question_deleted(sender, instance, **kwargs):
	static_dir = 'contest/static/teams'
	new_dir = 'question'+str(instance.id)
	new_dir_path = os.path.join(static_dir, instance.username)
	try:
		shutil.rmtree(new_dir_path)
	except OSError as e:
		print(e)