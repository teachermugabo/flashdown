from flashdown.forms import RegistrationForm, LoginForm

def get_and_delete(d, key, default):
    """Utility method to remove an entry for a dict and return it, returning the default value
    if d[key] doesn't exist of if it maps to None. Works similar to d.get(key, default) except that it
    removes the mapping as well. Used mainly to get and remove session data.
    """
    if key in d:
        result = d[key]
        del d[key]
        if result is not None:
            return result
        else:
            return default
    else:
        return default

def get_login_forms(request):
    """Adds login and registration forms to the given context.

    Adds optional bound forms and errors, if they exist. Otherwise
    it provides blank forms.
    """

    lform = get_and_delete(request.session, 'lform', LoginForm())
    rform = get_and_delete(request.session, 'rform', RegistrationForm())
    lform_errors = get_and_delete(request.session, 'lform_errors', None)
    rform_errors = get_and_delete(request.session, 'rform_errors', None)

    return {'login_form' : lform, 'registration_form' : rform,
            'login_errors' : lform_errors, 'registration_errors' : rform_errors}



