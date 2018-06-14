from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import View
from .models import team
from .static.functions import *
from django.db import IntegrityError

# Create your views here.

def index(request):
	return render(request, 'contest/register.html')

def login(request):
	if request.method == 'POST':
		team_name = request.POST.get('team_name')
		pwd = request.POST.get('password')

		if isBlank(team_name) or isBlank(pwd):
			return render(request, 'contest/register.html',{
				'hello' : 'You mad bro?!',
				'error_message' : 'You have left one or more field blank. Fix those! NOW!',
			})

		try:
			p = team.objects.get(teamId=team_name, password=pwd)
		except team.DoesNotExist:
			return render(request, 'contest/register.html',{
				'hello' : 'Invalid Credentials!',
				'error_message' : 'The Team Name and password combination you entered does not exist.',
			})
		request.session['team_name'] = p.teamId
		return render(request, 'contest/contest.html')
	else:
		return render(request, 'contest/register.html',{
				'hello' : 'Restricted!',
				'error_message' : 'You are trying to access a page that requires authentication.',
			})


def register(request):
	team_name = request.POST.get('team_name')
	p_w = request.POST.get('pwd')
	if isBlank(team_name) or isBlank(p_w):
		return render(request, 'contest/register.html',{
			'hello' : 'You mad bro?!',
			'error_message' : 'You have left one or more field blank. Fix those! NOW!',
		})
	elif (' ' in team_name) == True:
		return render(request, 'contest/register.html',{
			'hello' : 'Neccessities! :(',
			'error_message' : 'Team names cannot have spaces in them. Spaces are evil!',
		})
	elif(len(p_w)<8):
		return render(request, 'contest/register.html',{
			'hello' : 'Don\'t be lazy!',
			'error_message' : 'Your password should atleast be 8 characters long.',
		})
	try:
		team_instance = team(teamId=team_name, password=p_w)
		team_instance.save();
	except IntegrityError:
		return render(request, 'contest/register.html',{
			'hello' : 'Your Bad!',
			'error_message' : 'The team name "'+team_name+'" has already been taken, you have to choose a different one. :(',
		})	
	except Exception as e:
		return render(request, 'contest/register.html',{
			'error_message' : e,
		})	
	return render(request, 'contest/register.html',{
			'success' : 'success',
		})	


def logot(request):
    try:
        del request.session['team_name']
        request.session.modified = True
    except KeyError:
        pass
    
    return render(request, 'contest/register.html')