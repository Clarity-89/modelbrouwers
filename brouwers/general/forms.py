from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from models import UserProfile

from django.utils.translation import ugettext_lazy as _

class UserProfileForm(UserCreationForm):
	forum_nickname = forms.CharField(required=True,min_length=3, max_length=20)
	exclude_from_nomination = forms.BooleanField(required=False)
	email = forms.EmailField(label=_("E-mail"), max_length=75, required=False)
	
	def clean_forum_nickname(self):
		nickname = self.cleaned_data['forum_nickname']
		try:
			UserProfile.objects.get(forum_nickname=nickname)
			raise forms.ValidationError(_("Deze forumnickname is al in gebruik bij een andere user op deze website."))
			return nickname
		except UserProfile.DoesNotExist:
			return nickname
		
	
	def save(self, commit=False):
		user = super(UserProfileForm, self).save(commit=False)
		user.save()
		profile = UserProfile(user=user)
		profile.forum_nickname = self.cleaned_data['forum_nickname']
		if self.cleaned_data['exclude_from_nomination']:
			profile.exclude_from_nomination = True
		profile.save()
		return user

class ProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		exclude = ('user', 'last_vote', 'forum_nickname')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields =('email', 'first_name', 'last_name')
        widgets = {
        	'email': forms.TextInput(attrs={'size':30})
        }