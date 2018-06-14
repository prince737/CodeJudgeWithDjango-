from django.db import models

# Create your models here.
class team(models.Model):


	teamId = models.CharField(max_length=200, unique = True)
	password = models.CharField(max_length=30)

	REQUIRED_FIELDS = ('teamId','password',)
	USERNAME_FIELD = ('teamId',)