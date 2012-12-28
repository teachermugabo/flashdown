from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from decks.models import Tag, Card
from django.utils import simplejson

def overview(request):
    decks = Tag.objects.filter(is_deck=True)
    # do we need the RequestContext?
    return render_to_response('decks/overview.html',
                              {'decks' : decks},
                              context_instance=RequestContext(request))

def add_cards(request, deck_id=None):
    if deck_id is None:
        deck_id = request.COOKIES.get('active-deck-id', None)

    decks = Tag.objects.filter(is_deck=True)

    if deck_id is None:
        if decks.count() > 0:
            deck_id = decks[0].id

    if deck_id is not None:
        deck_id = int(deck_id)

    if decks == []:
        deck_id = None

    return render_to_response('decks/addcards.html',
                              {'decks': decks, 'active_deck_id': deck_id},
                              context_instance=RequestContext(request))

def update_card(request, card_id=None):
    pass

def review(request, deck_id):
    pass

def get_cards(request, deck_id):
    pass

def browse(request, deck_id=None):
    if deck_id is None:
        deck_id = request.COOKIES.get('active-deck-id', None)

    print('browse active: ' + str(deck_id))

    decks = Tag.objects.filter(is_deck=True)
    deck = None
    cards = None

    if deck_id is not None:
        deck = Tag.objects.get(pk=deck_id)
        if not deck.is_deck:  #TODO: do we care if we're browsing decks vs tags?
            return HttpResponse(code=400)
    elif decks.count() > 0:
         # no deck_id, no active deck cookie - just get the first one
        deck = decks[0]
        deck_id = deck.id

    if deck:
        cards = deck.deck_cards.filter(deleted=False)

    if deck_id is not None and deck_id != '':
        deck_id = int(deck_id)  # template will compre this to deck.id

    return render_to_response('decks/browse.html',
                              {'decks': decks, 'deck': deck,
                               'cards': cards, 'active_deck_id': deck_id})

def cards(request, deck_id):
    deck = Tag.objects.get(pk=deck_id)
    if not deck.is_deck:  #TODO: do we care? change this method to view-tag?
        return HttpResponse(code=400)

    #cards = deck.deck_cards.all()
    cards = deck.deck_cards.filter(deleted=False)
    return render_to_response('decks/browse.html',
                              {'deck' : deck, 'cards' : cards})




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

    deck_name = request.POST["deck_name"]
    deck = None
    try:
        deck = Tag.objects.get(name=deck_name)
        return HttpResponse() # already exists, don't send a new list item
    except Tag.DoesNotExist:
        deck = Tag(name=deck_name, is_deck=True)
        deck.save()

    return render_to_response('decks/deckinfo_partial.html', {'deck' : deck})


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


# vim: set ai et ts=4 sw=4 sts=4 :

