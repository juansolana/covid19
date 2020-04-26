from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import Person
from .forms import SymptonsForm, SignUpForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView
from django.contrib.gis.geos import fromstr

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string

from django.contrib.auth.decorators import login_required

from .utilities import to_geojson, update_mapbox
# Create your views here.

def default_map(request):
    # TODO: move this token to Django settings from an environment variable
    # found in the Mapbox account settings and getting started instructions
    # see https://www.mapbox.com/account/ under the "Access tokens" section
    mapbox_access_token = 'pk.eyJ1IjoianVhbnNvbGFuYSIsImEiOiJjazhncjR0enIwNGsxM2dvNHBqaXg0MGoxIn0.Y4m5LDMN6czSQhS7aAx0dw'
    return render(request, 'default.html',
                  {'mapbox_access_token': mapbox_access_token})

def get_persons(request):
    mapbox_access_token = 'pk.eyJ1IjoianVhbnNvbGFuYSIsImEiOiJjazhncjR0enIwNGsxM2dvNHBqaXg0MGoxIn0.Y4m5LDMN6czSQhS7aAx0dw'
    persons = Person.objects.all()
    return render(request, 'default.html', {'persons': persons, 'mapbox_access_token': mapbox_access_token})

def add_case_map(request):
    mapbox_access_token = 'pk.eyJ1IjoianVhbnNvbGFuYSIsImEiOiJjazhncjR0enIwNGsxM2dvNHBqaXg0MGoxIn0.Y4m5LDMN6czSQhS7aAx0dw'
    return render(request, 'add_case.html',
                  {'mapbox_access_token': mapbox_access_token})

def update_db(request):
    if (request.GET.get('save_person')):
        print('Button clicked')

@login_required(login_url='/login')
def symptons_view(request):
    user = request.user
    print (user.username, user.id)
    person, created = Person.objects.get_or_create(user_id=user.id)
    print(person.name, person.id, person.temperature)
    form = SymptonsForm(request.POST, person)
    print ('Valid Form: ', form.is_valid())
    if form.is_valid():
        temperature = form.cleaned_data.get('temperature')
        latitude = form.cleaned_data.get('latitude')
        longitude = form.cleaned_data.get('longitude')
        print ('From form: ', latitude, longitude)
        # location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
        location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
        temp = request.POST['temperature']
        # lon = request.POST.longitude
        print ('Temperature from post: ', temp)
        print (request.POST)
        person.latitude = latitude
        person.longitude = longitude
        person.location = location
        person.temperature = temperature
        person.name = user.username
        person.curp = 'SOCJ901031GP4'
        person.save()
        print(person.name, person.id, person.temperature, person.location)
        to_geojson()
        update_mapbox()
        return redirect('default')
    else:
        form = SymptonsForm(instance=person)
    return render(request, 'add_case.html', {'form':form})


########## LOGIN & LOGOUT################################
def login_view(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                login(request, user)
                # Y le redireccionamos a la portada
                return redirect('default')

    # Si llegamos al final renderizamos el formulario
    return render(request, "login.html", {'form': form})

def logout_view(request):
    logout(request)
    return redirect('default')

########## SIGNUP ###############################

def activation_sent_view(request):
    return render(request, 'activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.person.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('default')
    else:
        return render(request, 'activation_invalid.html')

def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            # user.profile.first_name = form.cleaned_data.get('first_name')
            # user.profile.last_name = form.cleaned_data.get('last_name')
            user.person.email = form.cleaned_data.get('email')
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            message = render_to_string('activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

