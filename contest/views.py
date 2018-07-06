from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.contrib.auth import login as auth_login,logout as auth_logout,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import question, timeRemaining, submission
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
		print(request.user)
		submit = submission.objects.get(user=request.user)
	except submission.DoesNotExist:
		submit = 'na'


	try:
		t = timeRemaining.objects.only('time').get(user=request.user)
		time = t.time
	except timeRemaining.DoesNotExist:
		dt = datetime.datetime.now()
		time = int(dt.strftime("%s")) * 1000
		a = timeRemaining.objects.create(user= request.user, time=time)
		a.save()


	context = {
		'submit' : submit,
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
		time = request.POST.get('time')

		
		#directory path of teams
		dir = "contest/static/teams/"+str(request.user)+"/"
		err = ''

		#setting input file
		if ciw.strip():
			ip = open("%sip.txt" %dir, "w+")
			ip.write(ciw)
			ip.seek(0)

		if event == "run":

			#writing code to file
			if mode == 'Python 3':
				f = open("%scode.py" %dir, "w+")
			elif mode == 'C / C++':
				f = open("%scode.cpp" %dir, "w+")
			elif mode == 'Java 8':
				f = open("%sMain.java" %dir, "w+")

			f.write(code)
			f.seek(0)

			#opening file for compilation output
			c = open("%scompile.txt" %dir, "w+")

			if mode == 'Python 3':
				call("cd '%s'; python3 -m py_compile code.py"%dir, shell=True, stdout=c, stderr=c)
			elif mode == 'C / C++':
				call("cd '%s'; g++ code.cpp"%dir, shell=True, stdout=c, stderr=c)
			elif mode == 'Java 8':
				call("cd '%s'; javac Main.java"%dir, shell=True, stdout=c, stderr=c)
							

			#output file
			o = open("%sop.txt" %dir, "w+")

			#check if compilation error exists
			if os.stat("%scompile.txt" %dir).st_size == 0:

				#check if custom input is supplied
				if os.path.isfile("%sip.txt" %dir):
					if mode == 'Python 3':
						call("cd '%s'; timeout 2s python3 code.py; echo $?" %dir, shell=True, stdin=ip, stdout=o, stderr=o)
					elif mode == 'C / C++':
						call("cd '%s'; timeout 2s ./a.out; echo $?" %dir, shell=True, stdin=ip, stdout=o, stderr=o)
					elif mode == 'Java 8':
						call("cd '%s'; timeout 2s java Main; echo $?" %dir, shell=True, stdin=ip, stdout=o, stderr=o)
					
					os.remove("%sip.txt" %dir)
					o.seek(0)
					data= o.read().splitlines()
					data = data[-1]
					if '124' in data[-3:]:
						context = {
							'op' : '<b>Your code took way too much time. Check for infinite loops or if proper input is supplied or try improving your algorithm.</b>',
							'err' : 'Time Limit Exceeded!',
						}

						#remvoing temp files and returning context		
						if mode == 'Python 3':
							os.remove("%scode.py" %dir)
						elif mode == 'C / C++':
							a=8
							os.remove("%scode.cpp" %dir)
							os.remove("%sa.out" %dir)
						elif mode == 'Java 8':
							os.remove("%sMain.java" %dir)
						os.remove("%sop.txt" %dir)
						os.remove("%scompile.txt" %dir)
						return JsonResponse(context, safe=False)

				else: 
					if mode == 'Python 3':
						call("cd '%s'; timeout 10s python3 code.py; echo $?" %dir, shell=True, stdout=o, stderr=o)
					elif mode == 'C / C++':
						call("cd '%s'; timeout 2s ./a.out; echo $?" %dir, shell=True, stdout=o, stderr=o)
					elif mode == 'Java 8':
						call("cd '%s'; timeout 2s java Main; echo $?" %dir, shell=True, stdout=o, stderr=o)
					o.seek(0)
					data= o.read().splitlines()
					data = data[-1]
					if '124' in data[-3:]:
						context = {
							'op' : '<b>Your code took way too much time. Check for infinite loops or if proper input is supplied or try improving your algorithm.</b>',
							'err' : 'Time Limit Exceeded!',
						}

						#remvoing temp files and returning context						
						if mode == 'Python 3':
							os.remove("%scode.py" %dir)
						elif mode == 'C / C++':
							a=8
							os.remove("%scode.cpp" %dir)
							os.remove("%sa.out" %dir)
						elif mode == 'Java 8':
							os.remove("%sMain.java" %dir)
						os.remove("%scompile.txt" %dir)
						os.remove("%sop.txt" %dir)
						return JsonResponse(context, safe=False)

				o.seek(0)
				data=o.read().strip()
				data=data[:-1]
			else:
				c.seek(0)
				data=c.read() #reading compilation error
				err = 'Compilation Error'

				#format output
			data = data.replace('	', '&nbsp;&nbsp;&nbsp;&nbsp;');
			data = data.replace(' ', '&nbsp;');
			data = data.replace('\n', '<br>');

			#preparing context
			context = {
				'op' : data,
				'err' : err,
			}
				
			#removing temp files
			
			if mode == 'Python 3':
				os.remove("%scode.py" %dir)
			elif mode == 'C / C++':
				os.remove("%scode.cpp" %dir)
				if err != 'Compilation Error':
					os.remove("%sa.out" %dir)
			elif mode == 'Java 8':
				os.remove("%sMain.java" %dir)
			os.remove("%sop.txt" %dir)
			os.remove("%scompile.txt" %dir)


		###'''''''''''Submission begins here''''''''''''###

		elif event == 'submit':
			dir = "contest/static/questions/question"+str(qid)+"/"
			ip = open("%sip.txt" %dir, "r")

			userdir = "contest/static/teams/"+str(request.user)+"/"


			if mode == 'C / C++':
				codefilename = str(qid)+'.cpp'
				codefile = "contest/static/teams/"+str(request.user)+"/"+str(qid)+'.cpp'
			elif mode == 'Python 3':
				codefilename = str(qid)+'.py'
				codefile = "contest/static/teams/"+str(request.user)+"/"+str(qid)+'.py'
			elif mode == 'Java 8':
				codefilename = 'Main.java'
				storefilename = str(qid)+'.java'
				codefile = "contest/static/teams/"+str(request.user)+"/Main.java"

			
			f = open("%s" %codefile, "w+")
			if mode == 'Java 8':
				s = open("%s%s" %(userdir,storefilename), "w+")
				s.write(code)
			f.write(code)
			f.seek(0)

			#compiling
			c = open("%scompile.txt" %userdir, "w+")
			if mode == 'C / C++':
				call("cd '%s'; g++ %s"%(userdir,codefilename), shell=True, stdout=c, stderr=c)
			elif mode == 'Python 3':
				call("cd '%s'; python3 -m py_compile %s"%(userdir, codefilename), shell=True, stdout=c, stderr=c)
			elif mode == 'Java 8':
				call("cd '%s'; javac Main.java"%userdir, shell=True, stdout=c, stderr=c)

			#setting output file
			opfile =  "contest/static/teams/"+str(request.user)+"/"+str(qid)+'.txt'
			o = open("%s" %opfile, "w+")

			#check if compilation error exists
			if os.stat("%scompile.txt"%userdir).st_size == 0:	
				if mode == 'C / C++':
					call("cd '%s'; timeout 2s ./a.out; echo $?" %userdir, shell=True, stdin=ip, stdout=o, stderr=o)
				elif mode == 'Python 3':
					call("cd '%s'; timeout 2s python3 %s; echo $?"%(userdir, codefilename), shell=True, stdin=ip, stdout=o, stderr=o)
				elif mode == 'Java 8':
					call("cd '%s'; timeout 2s java Main; echo $?" %userdir, shell=True, stdin=ip, stdout=o, stderr=o)		
				
				o.seek(0)
				data= o.read().splitlines()
				data = data[-1]
				if '124' in data[-3:]:
					context = {
						'op' : 'Time Limit Exceeded!',
						'err' : '',
					}
					setTime(request.user)
					os.remove("%scompile.txt" %userdir)
					os.remove("%s%s.txt" %(userdir,qid))
					os.remove("%s%s" %(userdir,codefilename))
					if mode == 'Java 8':
						os.remove("%sMain.class" %userdir)
						os.remove("%s%s" %(userdir,storefilename))
					elif mode == 'C / C++':
						os.remove("%sa.out" %userdir)
					return JsonResponse(context, safe=False)
			else:
				op = 'Compilation Error!'
				context = {
					'op' : op,
					'err' : '',
				}
				
				setTime(request.user)
				os.remove("%scompile.txt" %userdir)
				os.remove("%s%s.txt" %(userdir,qid))
				os.remove("%s%s" %(userdir,codefilename))
				if mode == 'Java 8':
					os.remove("%sMain.class" %userdir)
					os.remove("%s%s" %(userdir,storefilename))
				return JsonResponse(context, safe=False)

			#check if output matches
			req = open("%sop.txt" %dir, "r")
			reqOp = req.read().strip()

			o.seek(0)
			curOp = o.read().strip()

			if(reqOp == curOp):
				op = 'Accepted!'

				#updating submission model ***work on total time***
				try:
					submit = submission.objects.get(user=request.user)
					if qid=='1':
						submit.marks = submit.marks if submit.question1 else submit.marks+20
						submit.question1 = time
					elif qid=='2':
						submit.marks = submit.marks if submit.question2 else submit.marks+20
						submit.question2 = time
					elif qid=='3':
						submit.marks = submit.marks if submit.question3 else submit.marks+20
						submit.question3 = time
					elif qid=='4':
						submit.marks = submit.marks if submit.question4 else submit.marks+20
						submit.question4 = time
					else:
						submit.marks = submit.marks if submit.question5 else submit.marks+20
						submit.question5 = time
					submit.time = getTime(submit, time)
					submit.save()

				except submission.DoesNotExist:
					if qid=='1':
						submit_instance = submission.objects.create(user=request.user, question1=time, marks=20, time=time)
					elif qid=='2':
						submit_instance = submission.objects.create(user=request.user, question2=time, marks=20, time=time)
					elif qid=='3':
						submit_instance = submission.objects.create(user=request.user, question3=time, marks=20, time=time)
					elif qid=='4':
						submit_instance = submission.objects.create(user=request.user, question4=time, marks=20, time=time)
					else:
						submit_instance = submission.objects.create(user=request.user, question5=time, marks=20, time=time)	
					submit_instance.save()


				os.remove("%scompile.txt" %userdir)
				if mode == 'Java 8':
					os.remove("%sMain.class" %userdir)
					os.remove("%sMain.java" %userdir)
				elif mode == 'C / C++':
					os.remove("%sa.out" %userdir)
			else:
				op = 'Wrong Answer!'
				setTime(request.user)
				os.remove("%scompile.txt" %userdir)
				os.remove("%s%s.txt" %(userdir,qid))
				os.remove("%s%s" %(userdir,codefilename))
				if mode == 'Java 8':
					os.remove("%sMain.class" %userdir)
					os.remove("%s%s" %(userdir,storefilename))
				elif mode == 'C / C++':
					os.remove("%sa.out" %userdir)

			context = {
					'op' : op,
					'err' : '',
				}


		return JsonResponse(context, safe=False)

@login_required(login_url="/register/")
def rules(request):
	return render(request, 'contest/rules.html',)

def leaderboard(request):
	leaders = submission.objects.order_by('-marks', 'time')
	context = {
		'leaders' : leaders,
		'user' : request.user,
	}
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
	return redirect('/leaderboard/')
