from contest.models import question, timeRemaining, submission

def isBlank (s):
    if s and s.strip():
        return False
    return True

def setTime(user):
	try:
		submit = submission.objects.get(user=user)
		submit.penalty += 5
		if submit.time:
			submit_time = submit.time.split(':')
			if len(submit_time) == 3:
				minute = int(submit_time[1]) + 5
				hr = int(submit_time[0])
				if minute >= 60:
					hr = hr+1
					minute = minute % 60
				submit_time[0] = '0'+str(hr)
				submit_time[1] = str(minute) if minute>9 else '0'+str(minute)
				submit_time = ':'.join(submit_time)

			else:
				minute = int(submit_time[0]) + 5
				if minute >= 60:
					hr = 1
					minute = minute % 60
					submit_time = '0'+str(hr)+':'+str(minute) if minute>9 else '0'+str(minute)+':'+submit_time[1]
				else:
					submit_time[0] = str(minute) if minute>9 else '0'+str(minute)
					submit_time = ':'.join(submit_time)
			
		else:
			submit_time = '0'+str(submit.penalty)+':00'

		submit.time = submit_time
		submit.save()
	except submission.DoesNotExist:
		submit_instance = submission.objects.create(user=user, penalty=5, time='05:00')
		submit_instance.save()

def getTime(submit, time):
	if submit.penalty == 0:
		return time
	else:
		print(time)
		submit_time = time.split(':')
		print(submit_time)
		if len(submit_time) == 3:
			minute = int(submit_time[1]) + submit.penalty
			hr = int(submit_time[0])
			if minute >= 60:
				hr = hr+1
				minute = minute % 60
			submit_time[0] = '0'+str(hr)
			submit_time[1] = str(minute) if minute>9 else '0'+str(minute)
			submit_time = ':'.join(submit_time)
		else:
			minute = int(submit_time[0]) + submit.penalty
			if minute >= 60:
				hr = 1
				minute = minute % 60
				submit_time = '0'+str(hr)+':'+str(minute) if minute>9 else '0'+str(minute)+':'+submit_time[1]
			else:
				submit_time[0] = str(minute) if minute>9 else '0'+str(minute)
				submit_time = ':'.join(submit_time)

		return submit_time
