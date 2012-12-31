from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from decks.models import Tag, Card
from django.utils import simplejson
from django.views.decorators.csrf import ensure_csrf_cookie

# Note: ensure_csrf_cookie required if template doesn't have forms
# containing the csrf_token tag. Forgetting about this has caused
# problems in the past so I'm leaving it here to prevent problems caused
# by future refactoring of templates.
@ensure_csrf_cookie
def overview(request):
    decks = Tag.objects.filter(is_deck=True, deleted=False)
    # do we need the RequestContext?
    return render_to_response('decks/overview.html',
                              {'decks' : decks},
                              context_instance=RequestContext(request))

@ensure_csrf_cookie
def add_cards(request, deck_id=None):
    if deck_id is None:
        deck_id = request.COOKIES.get('active-deck-id', None)

    # TODO: what if we're passed some random string here using this cookie?

    decks = Tag.objects.filter(is_deck=True)

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


    return render_to_response('decks/addcards.html',
                              {'decks': decks, 'active_deck_id': deck_id},
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
    print(card_id)
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

# vim: set ai et ts=4 sw=4 sts=4 :

