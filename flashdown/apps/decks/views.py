from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest

from apps.decks.models import Deck, Card
from libs.login import get_login_forms
from libs.utils import get_object_or_None
from libs.decorators import ajax_request, login_required

import functools
login_required = functools.partial(login_required, url_name='overview')


#TODO: add splash page and make this login_required as well
def overview(request):
    """Renders the main dashboard page."""
    decks = Deck.objects.filter(active=True)
    ctx = {'decks': decks}
    ctx.update(get_login_forms(request))
    return render(request, 'decks/overview.html', ctx)

@login_required
def add_cards(request, deck_id=None):
    """Card editing page. User can add new cards to their decks."""
    (deck_id, __, decks) = resolve_deck_id(request, deck_id)
    ctx = {'decks': decks, 'active_deck_id': deck_id}
    ctx.update(get_login_forms(request))

    request.session['active_deck_id'] = deck_id

    return render(request, 'decks/addcards.html', ctx)

@login_required
def browse(request, deck_id=None):
    """Browse decks and their associated cards."""
    (deck_id, deck, decks) = resolve_deck_id(request, deck_id)
    cards = deck.deck_cards.filter(active=True) if deck else None

    request.session['active_deck_id'] = deck_id

    ctx = {'decks': decks, 'deck': deck,
           'cards': cards, 'active_deck_id': deck_id}
    ctx.update(get_login_forms(request))

    return render(request, 'decks/browse.html', ctx)


@login_required
def review(request, deck_id):
    """Review/study a given deck."""
    deck = get_object_or_404(Deck, pk=deck_id, active=True)
    cards = deck.deck_cards.filter(active=True)
    #TODO: if len(cards) == 0, in review.html show message that there's nothing to review

    request.session['active_deck_id'] = deck_id

    return render(request, 'decks/review.html', {'deck': deck, 'cards': cards})


###################################
# Primarily AJAX Functions        #
###################################

#TODO: unused
@ajax_request
def get_cards(request, deck_id):
    """Get a json list of cards for a given deck."""
    deck = Deck.objects.get_object_or_404(pk=deck_id, active=True)
    cards = deck.deck_cards.filter(active=True).values();
    deck = deck.values()
    return {'deck': deck, 'cards': cards}


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

    request.session['active_deck_id'] = deck.pk
    print(deck.pk)

    return render(request, 'decks/deckinfo_partial.html', {'deck' : deck})


@ajax_request
def delete_deck(request, deck_id):
    if not request.user.is_authenticated():
        return HttpResponse(status=401)

    if not request.is_ajax() or request.method != 'POST':
        return HttpResponseBadRequest()

    deck = get_object_or_404(Deck, pk=deck_id, active=True)
    deck.active = False # keep it around in case we want to restore it later
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

    card = Card(front=front, back=back, deck=deck, owner=request.user)
    card.save()

    #todo: store additional tags

    request.session['active_deck_id'] = deck_id

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
    card.active = False # keep it around in case we want to restore it later
    card.save()

    request.session['active_deck_id'] = deck_id

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


## Utility Methods ##

def resolve_deck_id(request, deck_id):
    """
    Returned deck_id is first of these that is valid:
    [stored active deck id, id of first deck], else None.
    Returns deck_id and the list of decks.
    """
    # TODO: what if we're passed some random string here using this cookie?
    # duh, use session storage to be safe

    if deck_id is None:
        deck_id = request.session.get('active_deck_id', None)

    decks = Deck.objects.filter(active=True)
    deck = None

    # first try, using the given deck id
    if deck_id:
        try:
            deck = Deck.objects.get(pk=deck_id, active=True)
        except Deck.DoesNotExist:
            deck_id = None   # we got an invalid id

    # next try, using the first active deck
    if not deck_id and len(decks) > 0:
        deck_id = decks[0].pk
        deck = decks[0]

    deck_id = int(deck_id) if deck_id else None

    return (deck_id, deck, decks)


# vim: set ai et ts=4 sw=4 sts=4 :
