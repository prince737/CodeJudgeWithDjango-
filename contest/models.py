from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import os, shutil, errno


# Create your models here.
class team(models.Model):
	teamId = models.CharField(max_length=200, unique = True)
	password = models.CharField(max_length=30)

	REQUIRED_FIELDS = ('teamId','password',)
	USERNAME_FIELD = ('teamId',)


class question(models.Model):
	statement = models.CharField(max_length=5000, unique = True)


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