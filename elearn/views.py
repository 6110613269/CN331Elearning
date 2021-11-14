from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
# Create your views here.

def index(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse("login"))
	user = User.objects.get(username = request.user.username)
	usersub = user.subjectsubscribe_set.all()
	a= ""
	for i in usersub:
		a = i.notification_set.all()
		# print("i:",dir(a))
	# print("no:",dir(usersub))
	return render(request, "elearn/index.html", {
		"noti": a
	})
	
		

def deletenoti(request, id):
    obj = Notification.objects.get(id = id)
    obj.delete()
    return redirect('index')


def about(request):
	print("hello")
	return render(request,"elearn/about.html")

def logout_request(request):
	logout(request)
	return render(request, "elearn/index.html", {"message": "Log out."})

def signup_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user, backend='django.contrib.auth.backends.ModelBackend')
			#messages.success(request, "Registration successful." )
			return render(request, "elearn/index.html", {"message": "Registration successful."})
		#else :
			#messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm
	return render (request=request, template_name="elearn/signup.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return render(request, "elearn/index.html")
			else:
				return render(request, "elearn/login.html", {
                            "message": "Invalid username or password."
                        })
		else:
			return render(request, "elearn/login.html", {
                            "message": "Invalid username or password."
                        })
	form = AuthenticationForm()
	return render(request=request, template_name="elearn/login.html", context={"login_form":form})

# def password_reset_request(request):
# 	if request.method == "POST":
# 		password_reset_form = PasswordResetForm(request.POST)
# 		if password_reset_form.is_valid():
# 			data = password_reset_form.cleaned_data['email']
# 			associated_users = User.objects.filter(Q(email=data))
# 			if associated_users.exists():
# 				for user in associated_users:
# 					subject = "Password Reset Requested"
# 					email_template_name = "elearn/password/password_reset_email.txt"
# 					c = {
# 					"email":user.email,
# 					'domain':'elearningcn321.herokuapp.com',
# 					'site_name': 'Website',
# 					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
# 					"user": user,
# 					'token': default_token_generator.make_token(user),
# 					'protocol': 'https',
# 					}
# 					email = render_to_string(email_template_name, c)
# 					try:
# 						send_mail(subject, email, '6110612980@student.tu.ac.th' , [user.email], fail_silently=False)
# 					except BadHeaderError:
# 						return HttpResponse('Invalid header found.')
# 					return render(request, "elearn/password/password_reset_done.html")
# 	password_reset_form = PasswordResetForm()
# 	return render(request=request, template_name="elearn/password/password_reset.html", context={"password_reset_form":password_reset_form})


def courselist(request):
    listsubject = SubjectSubscribe.objects.all()

	# data = request.POST.['q']
	# result = SubjectSubscribe.objects.filter(subjectid=search).order_by('id')

    for s in listsubject:
    	# print (s.subscriber.count())
    	# print ("user",request.user)
    	if s.subscriber.filter(id=request.user.id):
    		s.subscribe = False
    	else:
    		s.subscribe = True
    return render(request, "elearn/courselist.html",{
    	'list':listsubject
    })

def searchcourse(request):
	if request.method == "POST" :
		search = request.POST["searchcourse"]
		searchs = SubjectSubscribe.objects.filter(subjectid__contains=search)
		print ("search",search)
		print ("searchs",searchs)
		return render(request, "elearn/courselist.html", {
			"list" : searchs
			
		})
	else :
		return HttpResponseRedirect(reverse("courselist"))
		
# def searchfile(request):
# 	if request.method == "POST" :
# 		search = request.POST["searchfile"]
# 		searchs = SubjectSubScribe.objects.filter(subjectid__contains=search)
# 		return render(request, "elearn/courselist.html", {
# 			"searchs" : searchs
#                 })
# 	else :
# 		return HttpResponseRedirect(reverse("courselist"))

def bookcourselist(request, subjectid):
	course = SubjectSubscribe.objects.get(id=subjectid)
	# course.subscriber.add(request.user)
	if course.subscriber.filter(id=request.user.id):
		course.subscriber.remove(request.user)
	else:
		course.subscriber.add(request.user)


	print ("course",course.subscriber.count())
	return HttpResponseRedirect(reverse("courselist"))



def createsubject(request):
	if request.method == 'POST':
		form = CreateSubjectForm(request.POST, request.FILES)
		if form.is_valid:
			form.save()
			return redirect('courselist')
		else:
			print(form.errors)
	else:
		form = CreateSubjectForm()
	return render(request, 'elearn/createsubject.html', {
        'form': form
    })


def uploadfile(request):
	subjects = SubjectSubscribe.objects.all()
	if request.method == 'POST':
		form = FileForm(request.POST, request.FILES)
		subjectid = form['subjectid'].value()
		sid = SubjectSubscribe.objects.get(pk = subjectid)
		filename = form['filename'].value()
		if form.is_valid():
			notification(sid,filename, "file")
			form.save()
			# eachsubject(request, form['subjectid'].value())
			return redirect('courselist')
		else:
			print(form.errors)
	else:
		form = FileForm()
	return render(request, 'elearn/uploadfile.html', {
        'form': form,
        'subjects' : subjects
    })


def uploadvideo(request):
	subjects = SubjectSubscribe.objects.all()
	# print (usersub)
	if request.method == 'POST':
		form = VideoForm(request.POST, request.FILES)
		subjectid = form['subjectid'].value()
		sid = SubjectSubscribe.objects.get(pk = subjectid)
		videoname = form['videoname'].value()
		# print("subjectid:",subjectid)
		# print()
		if form.is_valid():
			notification(sid,videoname, "video")
			form.save()
			return redirect('courselist')
		else:
			print(form.errors)
	else:
		form = VideoForm()
	return render(request, 'elearn/uploadvideo.html', {
        'form': form,
        'subjects' : subjects
    })





def eachsubject(request, subjectid):

	subject = SubjectSubscribe.objects.get(id=subjectid)
	comments = Comments.objects.filter(subjectID=subject)
	videos = Video.objects.filter(subjectid=subject)
	files = File.objects.filter(subjectid=subject)

	return render(request, 'elearn/eachsubject.html', {
		'subject' : subject,
		'comments' : comments,
		'videos' : videos,
		'files' : files
		
	})

def searcheachsubject(request, subjectid):
	if request.method == "POST" :
		subject = SubjectSubscribe.objects.get(id=subjectid)
		comments = Comments.objects.filter(subjectID=subject)
		search = request.POST["searcheachsubject"]
		searchvideo = Video.objects.filter(videoname__contains=search)
		searchfile = File.objects.filter(filename__contains=search)
		return render(request, "elearn/eachsubject.html", {
			"videos" : searchvideo,
			"files"  : searchfile,
			"subject" : subject,
			"comments" : comments,
                })
	else :
		return HttpResponseRedirect(reverse("eachsubject"))
		

def commenteachsubject(request, subjectid):
	user = User.objects.get(id=request.user.id)
	subject = SubjectSubscribe.objects.get(id=subjectid)
	data = request.POST['body']
	comment = Comments.objects.create( body=data, username=request.user.username)
	comment.userID.add(user)
	comment.subjectID.add(subject)
	comment.save()
	return redirect('eachsubject', subjectid)


def editprofile(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()
            print("user:",user.first_name)
           
        return redirect("index")
    else:

        return render(request, "elearn/editprofile.html")


def notification( subjectid,name,types):
	newfile = subjectid.subjectid + " has uploaded a file " + name
	newvideo = subjectid.subjectid + " has uploaded a video " + name
	if types == "file":
		noti = Notification( message=newfile ,subjectid=subjectid)
		# print ("id:",subjectid)
		noti.save()
	if types == "video":
		noti = Notification( message=newvideo ,subjectid=subjectid)

		noti.save()

