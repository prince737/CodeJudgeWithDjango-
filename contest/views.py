from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.contrib.auth import login as auth_login,logout as auth_logout,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import team
from .static.functions import *
from django.db import IntegrityError


# Create your views here.



def register(request):
	if request.method == 'POST':
		team_name = request.POST.get('team_name')
		password = request.POST.get('pwd')
		if isBlank(team_name) or isBlank(password):
			return render(request, 'contest/register.html',{
				'hello' : 'You mad bro?!',
				'error_message' : 'You have left one or more field blank. Fix those! NOW!',
			})
		elif (' ' in team_name) == True:
			return render(request, 'contest/register.html',{
				'hello' : 'Neccessities! :(',
				'error_message' : 'Team names cannot have spaces in them. Spaces are evil!',
			})
		elif(len(password)<8):
			return render(request, 'contest/register.html',{
				'hello' : 'Don\'t be lazy!',
				'error_message' : 'Your password should atleast be 8 characters long.',
			})
		try:
			team_instance = User.objects.create_user(username=team_name, password=password)
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
	elif request.method == 'GET':
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

		user = authenticate(request, username=team_name, password=pwd)
		if user is not None:
			auth_login(request, user)
			return redirect('/contest/begin/')
		else:
			return render(request, 'contest/register.html',{
				'hello' : 'Invalid Credentials!',
				'error_message' : 'The Team Name and password combination you entered does not exist.',
			})
		
	elif not request.user.is_authenticated:
		return render(request, 'contest/register.html',)

@login_required(login_url="/register/")
def contest_begin(request):
	context = {}
	context['user'] = request.user
	return render(request, 'contest/contest.html', context)

def logout(request):
    try:
        auth_logout(request)
    except KeyError:
        pass
    
    return render(request, 'contest/register.html')


'''
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
	elif 'team_name' not in request.session:
		 return redirect('https://google.com/')


def register(request):
	if request.method == 'POST':
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
	elif request.method == 'GET':
		return render(request, 'contest/register.html',)	


def logout(request):
    if 'team_name' not in request.session:
        request.session.flush()
        request.session.modified = True
    
    return redirect('/register/')
    '''