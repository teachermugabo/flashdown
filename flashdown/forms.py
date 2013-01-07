
from django import forms
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper


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



