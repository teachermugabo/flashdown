from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView

def home(request):
    # TODO: make a splash page
    return HttpResponseRedirect(reverse('overview'))

handler500 = TemplateView.as_view(template_name="500.html")
