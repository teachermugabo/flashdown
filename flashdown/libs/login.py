from flashdown.forms import LoginForm, RegistrationForm
from libs.utils import get_and_delete

def get_login_forms(request):
    """
    Retrieve login and registration forms and erros from the current session.
    Returns blank forms if none exist.
    """

    lform = get_and_delete(request.session, 'lform', LoginForm())
    rform = get_and_delete(request.session, 'rform', RegistrationForm())
    lform_errors = get_and_delete(request.session, 'lform_errors', None)
    rform_errors = get_and_delete(request.session, 'rform_errors', None)

    return {'login_form' : lform, 'registration_form' : rform,
            'login_errors' : lform_errors, 'registration_errors' : rform_errors}



