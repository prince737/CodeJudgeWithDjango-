from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.contrib.auth import login as auth_login,logout as auth_logout,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import question, timeRemaining
from .static.functions import *
from django.db import IntegrityError
import os, shutil, errno
from django.http import JsonResponse
from subprocess import *
import datetime
from filecmp import *



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
			
			try:
				completion_status = timeRemaining.objects.get(user=user.id)
				if completion_status.completion == True:
					return render(request, 'contest/register.html',{
						'hello' : 'Oh snap!',
						'error_message' : 'Looks like have already completed prelims. Please wait for the results to be announced.',
					})
			except timeRemaining.DoesNotExist:
				pass
			
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


	try:
		t = timeRemaining.objects.only('time').get(user=request.user)
		time = t.time
	except timeRemaining.DoesNotExist:
		dt = datetime.datetime.now()
		time = int(dt.strftime("%s")) * 1000
		a = timeRemaining.objects.create(user= request.user, time=time)
		a.save()


	context = {
		'questions' : questions,
		'user' : request.user,
		'time' : time,
	}
	if request.method == 'GET':
		return render(request, 'contest/contest.html', context)


	elif request.method == 'POST':
		code = request.POST.get('code')
		mode = request.POST.get('mode')
		qid = request.POST.get('qid')
		ciw = request.POST.get('ciw')
		event = request.POST.get('event')

		
		#directory path of teams
		dir = "contest/static/teams/"+str(request.user)+"/"
		err = ''

		#setting input file
		if ciw.strip():
			ip = open("%sip.txt" %dir, "w+")
			ip.write(ciw)
			ip.seek(0)

		if event == "run":
			if mode =='Python 3': 
				f = open("%scode.py" %dir, "w")
				f.write(code)

				#compile
				f = open("%sop.txt" %dir, "w+")

				#check if custom input is supplied and run accordingly
				if os.path.isfile("%sip.txt" %dir):
					print("here")
					call("cd '%s'; python3 code.py"%dir, shell=True, stdin=ip, stdout=f, stderr=f)
					os.remove("%sip.txt" %dir)
				else:
					call("cd '%s'; python3 code.py"%dir, shell=True, stdout=f, stderr=f)					

				#copy file contents to local variable
				f.seek(0)
				data=f.read()

				#format output
				data = data.replace('	', '&nbsp;&nbsp;&nbsp;&nbsp;');
				data = data.replace(' ', '&nbsp;');
				data = data.replace('\n', '<br>');

				#check if compilation error exixts
				if data.find('code.py') != -1:
					err = 'Compilation Error'

				#create context
				context = {
					'op' : data,
					'err' : err,
				}				

				#remove all temporary files
				os.remove("%sop.txt" %dir)
				os.remove("%scode.py" %dir)
				
			elif mode == 'C / C++':
				f = open("%scode.cpp" %dir, "w+")
				

				f.write(code)
				f.seek(0)

				c = open("%scompile.txt" %dir, "w+")
				call("cd '%s'; g++ code.cpp"%dir, shell=True, stdout=c, stderr=c)

				o = open("%sop.txt" %dir, "w+")

				#check if compilation error exists
				if os.stat("%scompile.txt" %dir).st_size == 0:

					#check if custom input supplied
					if os.path.isfile("%sip.txt" %dir):
						call("cd '%s'; ./a.out" %dir, shell=True, stdin=ip, stdout=o, stderr=o)
						os.remove("%sip.txt" %dir)
					else:
						call("cd '%s'; ./a.out" %dir, shell=True, stdout=o, stderr=o)
					o.seek(0)
					data=o.read()
				else:
					c.seek(0)
					data=c.read()
					err = 'Compilation Error'

				#format output
				data = data.replace('	', '&nbsp;&nbsp;&nbsp;&nbsp;');
				data = data.replace(' ', '&nbsp;');
				data = data.replace('\n', '<br>');

				context = {
					'op' : data,
					'err' : err,
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
					data=o.read()
				else:
					c.seek(0)
					data=c.read()
					err = 'Compilation Error'

				data = data.replace('	', '&nbsp;&nbsp;&nbsp;&nbsp;');
				data = data.replace(' ', '&nbsp;');
				data = data.replace('\n', '<br>');

				context = {
					'op' : data,
					'err' : err,
				}
				
				os.remove("%sop.txt" %dir)
				os.remove("%sMain.java" %dir)
				os.remove("%scompile.txt" %dir)

		###'''''''''''Submission begins here''''''''''''###

		elif event == 'submit':
			print(qid)
			dir = "contest/static/questions/question"+str(qid)+"/"
			ip = open("%sip.txt" %dir, "r")

			userdir = "contest/static/teams/"+str(request.user)+"/"


			if mode == 'C / C++':
				codefilename = str(qid)+'.cpp'
				codefile = "contest/static/teams/"+str(request.user)+"/"+str(qid)+'.cpp'
			elif mode == 'Python 3':
				codefilename = str(qid)+'.py'
				codefile = "contest/static/teams/"+str(request.user)+"/"+str(qid)+'.py'
			
			f = open("%s" %codefile, "w+")
			f.write(code)
			f.seek(0)

			#compiling
			c = open("%scompile.txt" %userdir, "w+")
			if mode == 'C / C++':
				codefilename = str(qid)+'.cpp'
				call("cd '%s'; g++ %s"%(userdir,codefilename), shell=True, stdout=c, stderr=c)
			elif mode == 'Python 3':
				codefilename = str(qid)+'.py'
				call("cd '%s'; python3 -m py_compile %s"%(userdir, codefilename), shell=True, stdout=c, stderr=c)

			#setting output file
			opfile =  "contest/static/teams/"+str(request.user)+"/"+str(qid)+'.txt'
			o = open("%s" %opfile, "w+")

			#check if compilation error exists
			if os.stat("%scompile.txt"%userdir).st_size == 0:	
				if mode == 'C / C++':
					call("cd '%s'; timeout 2s ./a.out; echo $?" %userdir, shell=True, stdin=ip, stdout=o, stderr=o)
				elif mode == 'Python 3':
					call("cd '%s'; timeout 2s python3 %s; echo $?"%(userdir, codefilename), shell=True, stdin=ip, stdout=o, stderr=o)		
				
				o.seek(0)
				data= o.read().splitlines()
				data = data[-1]
				if '124' in data:
					context = {
						'op' : 'Time Limit Exceeded!',
						'err' : '',
					}
					os.remove("%scompile.txt" %userdir)
					os.remove("%s%s.txt" %(userdir,qid))
					os.remove("%s%s" %(userdir,codefilename))
					return JsonResponse(context, safe=False)
			else:
				op = 'Compilation Error!'
				context = {
					'op' : op,
					'err' : '',
				}
				os.remove("%scompile.txt" %userdir)
				os.remove("%s%s.txt" %(userdir,qid))
				os.remove("%s%s" %(userdir,codefilename))
				return JsonResponse(context, safe=False)

			#check if output matches
			req = open("%sop.txt" %dir, "r")
			reqOp = req.read().strip()

			o.seek(0)
			curOp = o.read().strip()

			if(reqOp == curOp):
				op = 'Accepted!'
				os.remove("%scompile.txt" %userdir)
			else:
				op = 'Wrong Answer!'
				os.remove("%scompile.txt" %userdir)
				os.remove("%s%s.txt" %(userdir,qid))
				os.remove("%s%s" %(userdir,codefilename))

			context = {
					'op' : op,
					'err' : '',
				}


		return JsonResponse(context, safe=False)

@login_required(login_url="/register/")
def rules(request):
	return render(request, 'contest/rules.html',)

def leaderboard(request):
	context = {}
	context['user'] = request.user
	return render(request, 'contest/leaderboard.html', context)

def logout(request):
	try:
		 auth_logout(request)
	except KeyError:
		pass
	return render(request, 'contest/register.html')

def give_up(request):
	try:
		time = timeRemaining.objects.get(user=request.user)
		time.completion = True
		time.save()
		auth_logout(request)
	except timeRemaining.DoesNotExist:
		pass
	except KeyError:
		pass	
	return render(request, 'contest/register.html')

def lleaderboard(request):
	try:
		time = timeRemaining.objects.get(user=request.user)
		time.completion = True
		time.save()
		auth_logout(request)
	except timeRemaining.DoesNotExist:
		pass
	except KeyError:
		pass	
	return render(request, 'contest/leaderboard.html')
