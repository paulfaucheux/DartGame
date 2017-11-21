from django import forms

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
        


    