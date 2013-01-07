from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate
from django.contrib.auth.models import User
from django.template import RequestContext, loader
from django.shortcuts import render

from flashdown.forms import LoginForm, RegistrationForm
from libs.decorators import ajax_request


def home(request):
    ctx = {'login_form': LoginForm(), 'registration_form': RegistrationForm()}
    return render(request, 'index.html', ctx)

###################################
# Login / Logout / Reset Password #
###################################
@ajax_request
def login(request):
    """
    Log the user in. If successful, let the client handle the redirect.
    If login fails, return a JSON response indicating failure, along with
    the rendered html of the bound login form.
    """
    if request.user.is_authenticated() or request.method != 'POST':
        return {'success': True, 'redirect': reverse('overview')}

    form = LoginForm(request.POST)
    t = loader.get_template('login_modal.html')

    if not form.is_valid():
        c = RequestContext(request, {'login_form': form, 'form_only': True})
        form_html = t.render(c)
        return {'success': False, 'form_html': form_html}

    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    if not user:
        c = RequestContext(request, {'login_form': form, 'form_only': True,
                                     'extra_errors': ['Invalid password.']})
        form_html = t.render(c)
        return {'success': False, 'form_html': form_html}

    auth_login(request, user)
    return {'success': True, 'redirect': reverse('overview')}


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('index'))


@ajax_request
def register(request):
    """
    Register a new user. If successful, log the user in and let the client
    handle the redirect. If registration fails, return a JSON response indicating
    failure, along with the rendered html of the bound registration form.
    """
    if request.user.is_authenticated() or request.method != 'POST':
        return {'success': True, 'redirect': reverse('overview')}

    form = RegistrationForm(request.POST)
    t = loader.get_template('registration_modal.html')
    c = RequestContext(request, {'registration_form': form, 'form_only': True})
    form_html = t.render(c)

    if not form.is_valid():
        return {'success': False, 'form_html': form_html}

    # setup our new user and user profile
    user = User.objects.create_user(username=form.cleaned_data['username'],
                                    email=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'])
    user.save()

    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
    auth_login(request, user)

    return {'success': True, 'redirect': reverse('overview')}

