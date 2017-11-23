from django import forms

from darts.models import Dart

class SubmitPlayerForm(forms.Form):
    player1 = forms.CharField(label='Submit Player Name')
    player2 = forms.CharField(label='Submit Player Name')
    """
    player3 = forms.CharField(label='Submit Player Name')
    player4 = forms.CharField(label='Submit Player Name')
    player5 = forms.CharField(label='Submit Player Name')
    player6 = forms.CharField(label='Submit Player Name')
    player7 = forms.CharField(label='Submit Player Name')
    player8 = forms.CharField(label='Submit Player Name')
    """
    
    def clean(self): 
        cleaned_data = super(SubmitPlayerForm, self).clean()
        

class SubmitDart(forms.Form):
    dart1 = forms.CharField(label='Dart Played')
    
    def clean(self):
        cleaned_data = super(SubmitDart, self).clean()
    
    def clean_dart1(self):
        dart_value = self.cleaned_data['dart1']
        if (Dart.objects.get(DartName = str(dart_value)) == None):
            raise 'The dart entered does not exists'
        return dart_value
    