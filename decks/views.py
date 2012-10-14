from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from decks.models import Tag, Card

def overview(request):
    decks = Tag.objects.all()
    # do we need the RequestContext?
    return render_to_response('decks/overview.html',
                              {'decks' : decks},
                              context_instance=RequestContext(request))

def edit_card(request, deck_id, card_id=None):
    deck = get_object_or_404(Tag, pk=deck_id)

    if card_id is None:
        return render_to_response('decks/editcard.html', {'deck' : deck})
        #adding a new card

    card = get_object_or_404(Card, pk=card_id)
    if card.deck != deck:
        return HttpResponseBadRequest()

    return render_to_response('decks/editcard.html', {'card' : card, 'deck' : deck})


def view_deck(request, deck_id):
    deck = Tag.objects.get(pk=deck_id)
    if not deck.is_deck:  #TODO: do we care? change this method to view-tag?
        return HttpResponse(code=400)

    cards = deck.deck_cards.all()
    return render_to_response('decks/viewdeck.html', {'deck' : deck, 'cards' : cards})


def review_deck(request, deck_name):
    return render_to_response('decks/reviewdeck.html')


# ajax handlers
def new_deck(request):
    """process an ajax request to add a new deck"""
    if not request.is_ajax():
        return HttpResponse(status=400)

    if not request.POST:  # we need the post data
        return HttpResponse('')

    #TODO: validate data

    deck_name = request.POST["deck_name"]
    deck = None
    try:
        deck = Tag.objects.get(name=deck_name)
        return HttpResponse('') # already exists, don't send a new list item
    except Tag.DoesNotExist:
        deck = Tag(name=deck_name, is_deck=True)
        deck.save()

    return render_to_response('decks/deckinfo_partial.html', {'deck': deck})


def new_card(request, deck_id):
    pass


from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

import html5lib
from html5lib import sanitizer

@register.filter
@stringfilter
def sanitize(value):
    p = html5lib.HTMLParser(tokenizer=sanitizer.HTMLSanitizer)
        return p.parseFragment(value).toxml()
# vim: set ai et ts=4 sw=4 sts=4 :
