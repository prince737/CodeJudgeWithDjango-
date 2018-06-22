from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.contrib.auth import login as auth_login,logout as auth_logout,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import question
from .static.functions import *
from django.db import IntegrityError
import os, shutil, errno
from django.http import JsonResponse
from subprocess import *



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


		static_dir = 'contest/static/teams'
		new_dir_path = os.path.join(static_dir, team_name)
		try:
			oldmask = os.umask(000)
			os.mkdir(new_dir_path)
			os.umask(oldmask)
		except OSError as e:
			if e.errno != errno.EEXIST:
				pass
			else:
				print(e)	


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
			return redirect('/RulesAndRegulations/')
		else:
			return render(request, 'contest/register.html',{
				'hello' : 'Invalid Credentials!',
				'error_message' : 'The Team Name and password combination you entered does not exist.',
			})
		
	elif not request.user.is_authenticated:
		return render(request, 'contest/register.html',)

@login_required(login_url="/register/")
def contest_begin(request):
	questions = question.objects.all()
	context = {
		'questions' : questions,
		'user' : request.user,
	}
	if request.method == 'GET':
		return render(request, 'contest/contest.html', context)
	elif request.method == 'POST':
		code = request.POST.get('code')
		mode = request.POST.get('mode')
		qid = request.POST.get('qid')
		ciw = request.POST.get('ciw')
		event = request.POST.get('event')

		#print(code)

		dir = "contest/static/teams/"+str(request.user)+"/"

		if mode =='Python 3':
			f = open("%scode.py" %dir, "w")
			f.write(code)

			f = open("%sop.txt" %dir, "w+")
			call("cd '%s'; python3 code.py"%dir, shell=True, stdout=f, stderr=f)

			f.seek(0)
			data=f.readlines()
			print(type(data))

			context = {
				'op' : data,
			}
			
			os.remove("%sop.txt" %dir)
			os.remove("%scode.py" %dir)
		elif mode == 'C / C++':
			f = open("%scode.cpp" %dir, "w+")
			
			f.write(code)
			f.seek(0)

			c = open("%scompile.txt" %dir, "w+")
			call("cd '%s'; g++ code.cpp"%dir, shell=True, stdout=c, stderr=c)

			o = open("%sop.txt" %dir, "w+")
			if os.stat("%scompile.txt" %dir).st_size == 0:
				call("cd '%s'; ./a.out" %dir, shell=True, stdout=o, stderr=o)
				o.seek(0)
				data=o.readlines()
			else:
				c.seek(0)
				data=c.readlines()
			

			context = {
				'op' : data,
			}
			
			os.remove("%sop.txt" %dir)
			os.remove("%scode.cpp" %dir)
			os.remove("%scompile.txt" %dir)

		elif mode == 'Java 8':
			f = open("%sMain.java" %dir, "w+")
			
			f.write(code)
			f.seek(0)

			c = open("%scompile.txt" %dir, "w+")
			call("cd '%s'; javac Main.java"%dir, shell=True, stdout=c, stderr=c)

			o = open("%sop.txt" %dir, "w+")
			if os.stat("%scompile.txt" %dir).st_size == 0:
				call("cd '%s'; java Main" %dir, shell=True, stdout=o, stderr=o)
				o.seek(0)
				data=o.readlines()
			else:
				c.seek(0)
				data=c.readlines()
			

			context = {
				'op' : data,
			}
			
			os.remove("%sop.txt" %dir)
			os.remove("%sMain.java" %dir)
			os.remove("%scompile.txt" %dir)


		return JsonResponse(context, safe=False)

@login_required(login_url="/register/")
def rules(request):
	context = {}
	context['user'] = request.user
	return render(request, 'contest/rules.html', context)

def logout(request):
    try:
        auth_logout(request)
    except KeyError:
        pass
    
    return render(request, 'contest/register.html')

