from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate
from django.contrib.auth.models import User

from flashdown.forms import LoginForm, RegistrationForm


def home(request):
    # TODO: make a splash page
    return HttpResponseRedirect(reverse('overview'))

###################################
# Login / Logout / Reset Password #
###################################
def login(request):
    if request.user.is_authenticated() or request.method != 'POST':
        return HttpResponseRedirect(reverse('home'))

    form = LoginForm(request.POST)
    if not form.is_valid():
        request.session['lform'] = form
        return HttpResponseRedirect(reverse('home'))

    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    if user:
        auth_login(request, user)
    else:
        request.session['lform'] = form
        request.session['lform_errors'] = ['Invalid Password']

    return HttpResponseRedirect(reverse('home'))

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('home'))

def register(request):
    if request.user.is_authenticated() or request.method != 'POST':
        return HttpResponseRedirect(reverse('home'))

    form = RegistrationForm(request.POST)
    if not form.is_valid():
        request.session['rform'] = form
        return HttpResponseRedirect(reverse('home'))

    # setup our new user and user profile
    user = User.objects.create_user(username=form.cleaned_data['username'],
                                    email=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'])
    user.save()

    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
    auth_login(request, user)

    return HttpResponseRedirect(reverse('home'))


