from django import forms
from django.contrib.auth.forms import UserCreationForm
from . models import User
from . models import Game
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
import json

MAX_JSON_DATA_LEN = 2048

class SignUpForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class' : 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    OPTIONS = [
    ("0", "Player"),
    ("1", "Developer"),
    ]
    status = forms.ChoiceField(
            choices=OPTIONS,
            initial='0',
            widget=forms.Select(attrs={'class' : 'form-control'}),
            required=True,
            label='Status',
    )
    class Meta:
        model = User
        fields = ('username','email','status')


    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # Here we determine is the user player or developer
        if self["status"].data == '0' :
            user.isPlayer = True
        elif self["status"].data == '1' :
            user.isDeveloper = True
        else:
            raise forms.ValidationError("Status input not recognized")
        if commit:

            user.save()
        return user

class AddGameForm(forms.ModelForm):
    game_url = forms.URLField(label='Game URL', widget=forms.URLInput(attrs={'class' : 'form-control'}))
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class' : 'form-control'}))
    description = forms.CharField(label='Description',widget=forms.Textarea(attrs={'class' : 'form-control'}))
    developer_name = forms.CharField()
    developer_name.widget = forms.HiddenInput()
    price = forms.DecimalField(
        max_digits = 5,
        decimal_places=2,
        min_value=float(0.01),
        widget=forms.NumberInput(attrs={'class' : 'form-control'}))

    def clean_price(self):
        if self.cleaned_data.get('price') < float(0.01):
            raise ValidationError("Price must be a positive number.")
        return self.cleaned_data.get('price')

    class Meta:
        model = Game
        fields = ('game_url','name','description','price','developer_name')

class GameSaveForm(forms.Form):
    gameState = forms.CharField(required=True, widget=forms.HiddenInput(), max_length=MAX_JSON_DATA_LEN)

    #This is for applying gamestate into the form and returning appropriate errors
    #if the gamestate is faulty
    def clean_gameState(self):
        try:
            temp = json.loads(self.cleaned_data['gameState'])
        except ValueError:
            raise ValidationError("The game's state is not a valid JSON.")

        if len(self.cleaned_data['gameState']) > MAX_JSON_DATA_LEN:
            raise ValidationError("The JSON input is too large.")

        return self.cleaned_data['gameState']

class GameScoreForm(forms.Form):
    score = forms.FloatField(required=True, widget=forms.HiddenInput())
