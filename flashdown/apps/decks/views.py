from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.views.decorators.csrf import ensure_csrf_cookie

from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate
from django.contrib.auth.models import User

from apps.decks.models import Tag, Card
from apps.decks.forms import RegistrationForm, LoginForm, CustomRecoveryForm

from password_reset.views import Recover

# Note: ensure_csrf_cookie required if template doesn't have forms
# containing the csrf_token tag. Forgetting about this has caused
# problems in the past so I'm leaving it here to prevent problems caused
# by future refactoring of templates.
@ensure_csrf_cookie
def overview(request):
    """Renders the main page."""
    decks = Tag.objects.filter(is_deck=True, deleted=False)
    ctx = {'decks': decks}
    ctx.update(get_forms(request))
    return render_to_response('decks/overview.html', ctx,
                              context_instance=RequestContext(request))

@ensure_csrf_cookie
def add_cards(request, deck_id=None):
    if deck_id is None:
        deck_id = request.COOKIES.get('active-deck-id', None)

    # TODO: what if we're passed some random string here using this cookie?

    decks = Tag.objects.filter(is_deck=True, deleted=False)

    if deck_id is None:
        if decks.count() > 0:
            deck_id = decks[0].id
    else:
        try:
            Tag.objects.filter(pk=deck_id)
        except Tag.DoesNotExist:
            deck_id = None   # we got an invalid id

    if deck_id is not None:
        deck_id = int(deck_id)

    if decks == []:
        deck_id = None

    ctx = {'decks': decks, 'active_deck_id': deck_id}
    ctx.update(get_forms(request))
    return render_to_response('decks/addcards.html', ctx,
                              context_instance=RequestContext(request))

def review(request, deck_id):
    pass

def get_cards(request, deck_id):
    pass

def browse(request, deck_id=None):
    if deck_id is None:
        deck_id = request.COOKIES.get('active-deck-id', None)

    decks = Tag.objects.filter(is_deck=True, deleted=False)
    deck = None
    cards = None

    if deck_id is not None:
        try:
            deck = Tag.objects.get(pk=deck_id)
        except Tag.DoesNotExist:
            deck_id = None


    elif decks and len(decks) > 0:
         # no deck_id, no active deck cookie - just get the first one
        deck = decks[0]
        deck_id = deck.id

    if deck:
        if not deck.is_deck:  #TODO: do we care if we're browsing decks vs tags?
            deck = None
        else:
            cards = deck.deck_cards.filter(deleted=False)

    if deck_id is not None and deck_id != '':
        deck_id = int(deck_id)  # template will compre this to deck.id

    ctx = {'decks': decks, 'deck': deck,
           'cards': cards, 'active_deck_id': deck_id}
    ctx.update(get_forms(request))
    return render_to_response('decks/browse.html', ctx,
                              context_instance=RequestContext(request))

def cards(request, deck_id):
    deck = Tag.objects.get(pk=deck_id)
    if not deck.is_deck:  #TODO: do we care? change this method to view-tag?
        return HttpResponse(code=400)

    #cards = deck.deck_cards.all()
    cards = deck.deck_cards.filter(deleted=False)
    return render_to_response('decks/browse.html',
                              {'deck' : deck, 'cards' : cards})

###################################
# Login / Logout / Reset Password #
###################################
def login(request):
    if request.user.is_authenticated() or request.method != 'POST':
        return HttpResponseRedirect(reverse('overview'))

    form = LoginForm(request.POST)
    if not form.is_valid():
        return render_main_page(request, lform=form) # rerender the bound form with errors

    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    if user:
        auth_login(request, user)
        return HttpResponseRedirect(reverse('overview'))
    else:
        return render_main_page(request, lform=form, lform_errors=['Invalid Password'])

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('overview'))

def register(request):
    if request.user.is_authenticated() or request.method != 'POST':
        return HttpResponseRedirect(reverse('overview'))

    form = RegistrationForm(request.POST)
    if not form.is_valid():
        return render_main_page(request, rform=form)

    # setup our new user and user profile
    user = User.objects.create_user(username=form.cleaned_data['username'],
                                    email=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'])
    user.save()

    user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
    auth_login(request, user)

    return HttpResponseRedirect(reverse('overview'))

class RecoverView(Recover):
    form_class = CustomRecoveryForm  # to disallow social users from attempting password reset
    search_fields = ['username']
recover = RecoverView.as_view()


###################################
# Primarily AJAX Functions        #
###################################

def new_deck(request):
    """process an ajax request to add a new deck"""
    if not request.is_ajax():
        return HttpResponse(status=400)

    if not request.POST:  # we need the post data
        return HttpResponse('')

    #TODO: validate data

    # currently the max deck name length is 50 characters
    deck_name = request.POST["deck_name"][:50]
    deck = None
    try:
        deck = Tag.objects.get(name=deck_name, deleted=False) # will be 0 or 1 of these
        return HttpResponse(status=200) # already exists, don't send a new list item
    except Tag.DoesNotExist:
        deck = Tag(name=deck_name, is_deck=True)
        deck.save()

    return render_to_response('decks/deckinfo_partial.html', {'deck' : deck})

def delete_deck(request, deck_id):
    if not request.is_ajax() or request.method != 'POST':
        return HttpResponseBadRequest()

    deck = get_object_or_404(Tag, pk=deck_id, deleted=False)
    if not deck.is_deck:
        return HttpResponseBadRequest()

    deck.deleted = True # keep it around in case we want to restore it later
    deck.save()

    return HttpResponse() #status=200 OK


def new_card(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    deck_id = request.POST.get("deck-id")
    front = request.POST.get("front")
    back = request.POST.get("back")

    for v in [deck_id, front, back]:
        if v is None:
            return HttpResponseBadRequest('missing data')

    if deck_id == '':
        return HttpResponseBadRequest('malformed deck id')

    deck_id = int(deck_id)

    deck = get_object_or_404(Tag, pk=deck_id)
    if not deck.is_deck:
        return HttpResponseBadRequest()

    # sanitize data
    """
    this is no longer necessary since we're just storing markdown and
    rendering it later

    import html5lib
    from html5lib import sanitizer

    p = html5lib.HTMLParser(tokenizer=sanitizer.HTMLSanitizer)
    front = p.parseFragment(request.POST["front"]).toxml()
    back = p.parseFragment(request.POST["back"]).toxml()
    """

    # escape newlines or we'll have trouble when inserting this in javascript
    # later
    front = request.POST["front"]
#    front = front.replace('\r\n', '\n')
    back = request.POST["back"]
#    back = back.replace('\r\n', '\n')

    card = Card(front=front, back=back, deck=deck)
    card.save()
    card.tags.add(deck)

    #todo: store additional tags

    return HttpResponse(status=201) # Created


def get_card(request, card_id):
    try:
        card = Card.objects.get(pk=card_id, deleted=False)
    except Card.DoesNotExist:
        return HttpResponse(status=404)

    card = {'front': card.front, 'back': card.back}

    return HttpResponse(simplejson.dumps(card), mimetype="application/json")


def delete_card(request, deck_id, card_id):
    if not request.is_ajax() or request.method != 'POST':
        return HttpResponseBadRequest()

    deck = get_object_or_404(Tag, pk=deck_id)
    if not deck.is_deck:
        return HttpResponseBadRequest()

    card = get_object_or_404(Card, pk=card_id)
    try:
        if not card.tags.filter(name=deck.name):
            return HttpResponseBadRequest()
    except:
        pass

    card.deleted = True # keep it around in case we want to restore it later
    card.save()

    return HttpResponse() #status=200 OK


def update_card(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    card_id = request.POST.get('card_id')
    front = request.POST.get('front')
    back = request.POST.get('back')

    if card_id is None or front is None or back is None:
        return HttpResponseBadRequest()

    try:
        card = Card.objects.get(pk=card_id, deleted=False)
        card.front = front
        card.back = back
        card.save()
    except Card.DoesNotExist:
        return HttpResponse(status=404)

    return HttpResponse(status=200)


##############################################################
# Utility Methods                                            #
##############################################################
def render_main_page(request, lform=None, rform=None, lform_errors=None, rform_errors=None):
    """Utility method to redirect and render the main page with the given bound forms and their
    associated errors. lform_errors and rform_errors are additional errors that can't be detected
    in their respective form's clean methods.
    """
    # store them in the session data temporarily until we redirect
    # TODO - is there a better way to do this?
    request.session['lform'] = lform
    request.session['rform'] = rform
    request.session['lform_errors'] = lform_errors
    request.session['rform_errors'] = rform_errors
    # we want to redirect so we're not still at one of the user auth urls if authentication fails
    return HttpResponseRedirect(reverse('overview'))

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

def get_forms(request):
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


# vim: set ai et ts=4 sw=4 sts=4 :

