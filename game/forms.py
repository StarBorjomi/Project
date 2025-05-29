from django import forms

from . models import Try

class TryForm(forms.ModelForm):
	class Meta:
		model = Try

		fields = ["guess"]
		labels = {"guess": "It's your turn"}
		widget = {"guess": forms.NumberInput( attrs = {"class": "form-control", "placeholder": "Enter a number in a range from 0 to 100"})}