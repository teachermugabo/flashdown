from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def home(request):
    # TODO: make a splash page
    return HttpResponseRedirect(reverse('overview'))

