from django.core.mail import send_mail

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.http import HttpResponseRedirect
from shortcuts import render_to_response
from django.db.models import Q

from forms import ProfileForm, UserForm, UserProfileForm
from brouwers.awards.models import Project
from models import UserProfile
from brouwers.secret_santa.models import Participant

from datetime import date

#TODO: separate code for awards and secret santa

def register(request):
	if request.method=='POST':
		# hack to allow spaces in 'usernames' TODO: change nickname field to hidden field
		request.POST['username'] = str(request.POST['forum_nickname']).replace(' ', '_')
		print request.POST['username']
		form = UserProfileForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			new_user = authenticate(username = username, password = password)
			login(request, new_user)
			if new_user.get_profile().exclude_from_nomination:
				projects = Project.objects.filter(brouwer__iexact = new_user.get_profile().forum_nickname)
				for project in projects:
					project.rejected = True
					project.save()
			if form.cleaned_data['email']:
				subject = 'Registratie op xbbtx.be'
				message = 'Bedankt voor uw registratie op http://xbbtx.be.\n\nU hebt geregistreerd met de volgende gegevens:\n\nGebruikersnaam: %s\nWachtwoord: %s\n\nBewaar deze gegevens voor als u uw login en/of wachtwoord mocht vergeten.' % (username, password)
				sender = 'sergeimaertens@skynet.be'
				receiver = [form.cleaned_data['email']]
				send_mail(subject, message, sender, receiver, fail_silently=True)			
			return HttpResponseRedirect('/profile/')
	else:
		form = UserProfileForm()
	return render_to_response(request, 'general/register.html', {'form': form})

def custom_login(request):    
    next_page = request.REQUEST.get('next')
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure next_page isn't garbage.
            if not next_page or ' ' in next_page:
                next_page = settings.LOGIN_REDIRECT_URL
            from django.contrib.auth import login
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(next_page)
    else:
        form = AuthenticationForm(request)
    return render_to_response(request, 'general/login.html', {
        'form': form,
        'next': next_page,
    })

@user_passes_test(lambda u: u.is_authenticated(), login_url='/login/')
def profile(request):
	forms = {}
	if request.method=='POST':
		forms['profileform'] = ProfileForm(request.POST, instance=request.user.get_profile())
		forms['userform'] = UserForm(request.POST, instance=request.user)
		
		if forms['profileform'].is_valid():
			forms['profileform'].save()
			if forms['profileform'].cleaned_data['exclude_from_nomination']==True:
				projects = Project.objects.filter(brouwer__iexact=request.user.get_profile().forum_nickname)
				for project in projects:
					project.rejected = True
					project.save()
			if forms['profileform'].cleaned_data['secret_santa']==True:
				participants = Participant.objects.filter(Q(user__exact=request.user) & Q(year=date.today().year))
				if not participants:
					participant = Participant(user=request.user, year=date.today().year)
					participant.save()
			if forms['profileform'].cleaned_data['secret_santa']==False:
				participants = Participant.objects.filter(Q(user__exact=request.user) & Q(year=date.today().year))
				if participants:
					participants[0].delete()

		if forms['userform'].is_valid():
			forms['userform'].save()
		return render_to_response(request, 'general/profile.html', forms)
	else:
		forms['profileform'] = ProfileForm(instance=request.user.get_profile())
		forms['userform'] = UserForm(instance=request.user)
		return render_to_response(request, 'general/profile.html', forms)
		
def custom_logout(request):
	next_page = request.GET.get('next')
	if not next_page or ' ' in next_page:
		next_page = "/?logout=1"
	logout(request)
	return HttpResponseRedirect(next_page)
