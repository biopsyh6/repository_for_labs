import django.forms
from django.contrib.auth.models import User
from django.contrib.auth import forms
from cinema.models import Client, Review, Movie, Ticket, Session, Genre


class UserRegistrationForm(forms.UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)

class ProfileRegistrationForm(django.forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'surname', 'email', 'birth_date', 'phone_number', 'image')
        widgets = {'birth_date': django.forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
                   'image': django.forms.FileInput(attrs={'class':'form-control', 'required':False,})
                   }
        

class LoginForm(django.forms.Form):
    username = django.forms.CharField()
    password = django.forms.CharField(widget=django.forms.PasswordInput)

class ReviewForm(django.forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text', 'rate')

class MovieForm(django.forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'country', 'genre', 'duration', 'budget', 'poster', 'description', 'rating']
        widgets = {'image': django.forms.FileInput(attrs={'class':'form-control', 'required':False,})}

class TicketForm(django.forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['session', 'price', 'employee']

class SessionForm(django.forms.ModelForm):
    class Meta:
        model = Session
        fields = ['movie', 'hall', 'start_time', 'end_time']

class MovieFilterForm(django.forms.Form):
    genre = django.forms.ModelChoiceField(queryset=Genre.objects.all(), required=False)
    min_rating = django.forms.FloatField(required=False, min_value=0.0, max_value=10.0)
    max_rating = django.forms.FloatField(required=False, min_value=0.0, max_value=10.0)

class TicketFilterForm(django.forms.Form):
    min_price = django.forms.FloatField(required=False, min_value=0.0)
    max_price = django.forms.FloatField(required=False, min_value=0.0)
    date = django.forms.DateField(required=False, widget=django.forms.SelectDateWidget(years=range(2024, 2026)))

class ProfileForm(django.forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'surname', 'email', 'birth_date', 'phone_number', 'image')
        widgets = {'birth_date': django.forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
                   'image': django.forms.FileInput(attrs={'class':'form-control', 'required':False,})
                   }
        