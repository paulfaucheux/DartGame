from django import forms
from django.core.exceptions import ValidationError

from darts.models import Dart, RefGame

class SubmitPlayerForm(forms.Form):
    player1 = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder":"Player name (Required)*", "class":"form-control"}), required=True)
    player2 = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder":"Player name (Required)*", "class":"form-control"}), required=True)
    player3 = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder":"Player name", "class":"form-control"}), required=False)
    player4 = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder":"Player name", "class":"form-control"}), required=False)
    player5 = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder":"Player name", "class":"form-control"}), required=False)
    player6 = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder":"Player name", "class":"form-control"}), required=False)
    player7 = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder":"Player name", "class":"form-control"}), required=False)
    player8 = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder":"Player name", "class":"form-control"}), required=False)
    game    = forms.ChoiceField(label=''
        , widget=forms.Select(attrs={"placeholder":"Select your game", "class":"form-control"})
        , choices=[ (game.pk, game.GameName) for game in RefGame.objects.all() ])
    
    def clean(self): 
        cleaned_data = super(SubmitPlayerForm, self).clean()
        names = [cleaned_data.get('player1'), cleaned_data.get('player2'), cleaned_data.get('player3')
        , cleaned_data.get('player4'), cleaned_data.get('player5'), cleaned_data.get('player6')
        , cleaned_data.get('player7'), cleaned_data.get('player8')]
        names = [x for x in names if x]
        if len(names) != len(set(names)):
            raise ValidationError("Invalid Names: Make sure each name is unique")

        

class SubmitDart(forms.Form):
    dart1 = forms.CharField(label='Dart Played')
    
    def clean(self):
        cleaned_data = super(SubmitDart, self).clean()
    
    def clean_dart1(self):
        dart_value = self.cleaned_data['dart1']
        if (Dart.objects.get(DartName = str(dart_value)) == None):
            raise ValidationError("The dart entered does not exists")
        return dart_value
    