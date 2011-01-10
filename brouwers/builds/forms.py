from django import forms
from django.core.exceptions import ObjectDoesNotExist
from models import Build

import re

class BrouwerSearchForm(forms.Form):
	nickname = forms.CharField(max_length=20)

class BuildForm(forms.ModelForm):
	class Meta:
		model = Build
		exclude = ('profile', 'nomination')
		widgets = {
			'url': forms.TextInput(attrs={'size':70}),
			'title': forms.TextInput(attrs={'size':70}),
			'img1': forms.TextInput(attrs={'size':70}),
			'img2': forms.TextInput(attrs={'size':70}),
			'img3': forms.TextInput(attrs={'size':70}),
			}
	
	def clean_url(self):
		url = self.cleaned_data['url']
		match = re.search('modelbrouwers.nl/phpBB3/viewtopic.php\?f=(\d+)&t=(\d+)', url)
		if not match:
			raise forms.ValidationError("De url wijst niet naar een forumtopic.")
		else:
			matched_url = match.group(0)
			try:
				Build.objects.get(url__icontains = matched_url)
				raise forms.ValidationError("Dit brouwverslag is al opgenomen in de database.")
			except ObjectDoesNotExist:
				pass
		return url
	
	def clean_scale(self):
		scale = self.cleaned_data['scale']
		match = re.search('1:\d+', scale)
		if match:
			return scale
		else:
			match = re.search('1/\d+', scale)
			if not match:
				raise forms.ValidationError("Fout formaat van schaal, correct zijn: 1/24 of 1:48.")
		return scale