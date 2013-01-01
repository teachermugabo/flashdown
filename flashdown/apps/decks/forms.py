
from django import forms
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper

from password_reset.forms import PasswordRecoveryForm


class RegistrationForm(forms.Form):
    # all fields are required, but some are checked manually below, to avoid
    # redundant error messages in some situations
    username = forms.CharField(max_length=30, label="Username")
    email = forms.EmailField(max_length=75, label="Email", required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False), label="Confirm Password")

    # used by django-crispy-forms - gives us lots of control over how forms are rendered
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.help_text_inline = True
        self.helper.error_text_inline = True
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username', None)
        if not username:
            raise forms.ValidationError("Please enter a username.")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise forms.ValidationError("That username is already taken.")

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1', None)
        if not password1:
            raise forms.ValidationError("Enter a password.")
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2', None)
        if not password2:
            raise forms.ValidationError("Re-enter your password.")
        return password2

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Passwords must match.")

        # TODO - make sure the password conforms to our security requirements
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label="Username", required=True)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), label="Password", required=True)

    # used by django-crispy-forms - gives us lots of control over how forms are rendered
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.help_text_inline = True
        self.helper.error_text_inline = True
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username', None)
        if not username:
            raise forms.ValidationError("Invalid Username.")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Invalid Username.")

        return username


    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        if not password:
            raise forms.ValidationError("Please enter a password.")

        return password


class CustomRecoveryForm(PasswordRecoveryForm):

    # override the defaul password recovery from from django-password-reset
    # We only need to override this single method to ensure that we raise a
    # form validation error if the user is a facebook user
    def clean_username_or_email(self):
        # this will always be email, since that's how we set it up in our recovery view
        username = self.cleaned_data['username_or_email']
        user = self.get_user_by_username(username)

        # make sure we don't have a social user
        if user.social_auth.filter(provider="facebook"):
            raise forms.ValidationError('You are authenticated through Facebook. Please visit www.facebook.com to reset your password.')

        self.cleaned_data['user'] = user
        return username


