from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest

from apps.decks.models import Deck, Card
from libs.login import get_login_forms
from libs.utils import get_object_or_None
from libs.decorators import ajax_request
from libs.decorators import login_required

import functools
login_required = functools.partial(login_required, url_name='overview')


def overview(request):
    """Renders the main page."""
    decks = Deck.objects.filter(active=True)
    ctx = {'decks': decks}
    ctx.update(get_login_forms(request))
    return render(request, 'decks/overview.html', ctx)

@login_required
def add_cards(request, deck_id=None):
    if deck_id is None:
        deck_id = request.COOKIES.get('active-deck-id', None)

    # TODO: what if we're passed some random string here using this cookie?

    decks = Deck.objects.filter(active=True)

    if deck_id is None and len(decks) > 0:
        deck_id = decks[0].pk
    else:
        try:
            Deck.objects.get(pk=deck_id)
        except Deck.DoesNotExist:
            deck_id = None   # we got an invalid id

    if deck_id is not None:
        deck_id = int(deck_id)

    deck_id = deck_id if decks else None
    deck_id = int(deck_id) if deck_id else None

    ctx = {'decks': decks, 'active_deck_id': deck_id}
    ctx.update(get_login_forms(request))
    return render(request, 'decks/addcards.html', ctx)

@login_required
def review(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id, active=True)
    cards = deck.deck_cards.filter(active=True)
    #TODO: if len(cards) == 0, in review.html show message that there's nothing to review
    return render(request, 'decks/review.html', {'deck': deck, 'cards': cards})

def get_cards(request, deck_id):
    pass

@login_required
def browse(request, deck_id=None):
    if deck_id is None:
        deck_id = request.COOKIES.get('active-deck-id', None)

    decks = Deck.objects.filter(active=True)
    deck = None
    cards = None

    if deck_id is not None:
        try:
            deck = Deck.objects.get(pk=deck_id, active=True)
        except Deck.DoesNotExist:
            deck_id = None

    if deck_id is None and len(decks) > 0:
         # no deck_id, no active deck cookie - just get the first one
        deck_id = decks[0].pk
        deck = decks[0]

    cards = deck.deck_cards.filter(active=True) if deck else None

    if deck_id: # not None, not ''
        deck_id = int(deck_id)  # template will compare this to deck.id

    ctx = {'decks': decks, 'deck': deck,
           'cards': cards, 'active_deck_id': deck_id}
    ctx.update(get_login_forms(request))
    return render(request, 'decks/browse.html', ctx)


#TODO: unused
@ajax_request
def cards(request, deck_id):
    deck = Deck.objects.get_object_or_404(pk=deck_id, active=True, id_deck=True)
    cards = deck.deck_cards.filter(active=True).values();
    deck = deck.values()
    return {'deck': deck, 'cards': cards}


###################################
# Primarily AJAX Functions        #
###################################

@ajax_request
def new_deck(request):
    """process an ajax request to add a new deck"""
    if not request.POST:  # we need the post data
        return HttpResponse()

    #TODO: validate data

    # currently the max deck name length is 50 characters
    deck_name = request.POST["deck_name"][:50]
    deck = get_object_or_None(Deck, name=deck_name, owner=request.user)
    if deck:
        return HttpResponse() # already exists, don't send a new list item
    else:
        deck = Deck(name=deck_name, owner=request.user)
        deck.save()

    return render(request, 'decks/deckinfo_partial.html', {'deck' : deck})


@ajax_request
def delete_deck(request, deck_id):
    if not request.user.is_authenticated():
        return HttpResponse(status=401)

    if not request.is_ajax() or request.method != 'POST':
        return HttpResponseBadRequest()

    deck = get_object_or_404(Deck, pk=deck_id, active=True)
    deck.deleted = True # keep it around in case we want to restore it later
    deck.save()

    return HttpResponse() #status=200 OK


@ajax_request
def new_card(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    deck_id = request.POST.get("deck-id")
    front = request.POST.get("front")
    back = request.POST.get("back")

    if not all([deck_id, front, back]): # Not None, not ''
        return HttpResponseBadRequest('missing data')

    deck = get_object_or_404(Deck, pk=int(deck_id))

    card = Card(front=front, back=back, deck=deck)
    card.save()
    card.tags.add(deck)

    #todo: store additional tags

    return HttpResponse(status=201) # Created


@ajax_request
def get_card(request, card_id):
    card = get_object_or_404(Card, pk=card_id, active=True)
    return {'front': card.front, 'back': card.back}


@ajax_request
def delete_card(request, deck_id, card_id):
    if not request.is_ajax() or request.method != 'POST':
        return HttpResponseBadRequest()

    deck = get_object_or_404(Deck, pk=deck_id, active=True)
    card = get_object_or_404(Card, pk=card_id, active=True, deck=deck)
    card.deleted = True # keep it around in case we want to restore it later
    card.save()

    return HttpResponse()


@ajax_request
def update_card(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    card_id = request.POST.get('card_id')
    front = request.POST.get('front')
    back = request.POST.get('back')

    if not all([card_id, front, back]): # not None, not empty
        return HttpResponseBadRequest()

    card = get_object_or_404(Card, pk=card_id, active=True)
    card.front = front
    card.back = back
    card.save()

    return HttpResponse()

# vim: set ai et ts=4 sw=4 sts=4 :

