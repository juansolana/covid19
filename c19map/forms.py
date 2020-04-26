from django.contrib.gis import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Person
from django.contrib.gis.geos import fromstr
from mapbox_location_field.spatial.models import SpatialLocationField


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=150, help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class LoginForm():
    pass


class SymptonsForm(forms.ModelForm):

    temperature = forms.FloatField(min_value=36, max_value=45, help_text='Temperatura corporal', label='Temperatura', initial=36.5)
    edad = forms.IntegerField(help_text='Edad actual', label='Edad', initial=False, required=True, min_value=1, max_value=120)
    sexo = forms.ChoiceField(help_text='Género', label='Género', initial=False, required=False, choices=((1, ''), (2, 'Hombre'), (3, 'Mujer')))
    tos = forms.BooleanField(help_text='¿Tienes tos?', label='Tos', initial=False, required=False)
    dolor_cabeza = forms.BooleanField(help_text='¿Tienes dolor de cabeza?', label='Dolor de Cabeza', initial=False, required=False)
    dolor_garganta = forms.BooleanField(help_text='¿Tienes dolor de garganta?', label='Dolor de garganta', initial=False, required=False)
    respiracion = forms.BooleanField(help_text='¿Tienes dificultad para respirar?', label='Dificultad para Respirar', initial=False, required=False)
    latitude = forms.FloatField(initial=20, label='Latitud', required=False) #, disabled='disabled')
    longitude = forms.FloatField(initial=-105, label='Longitud', required=False) #, disabled='disabled')
    # location = SpatialLocationField()

    class Meta:
        model = Person
        fields = ['temperature', 'latitude', 'longitude','age', 'sexo',]