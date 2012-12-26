from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from decks.models import Tag, Card
from django.utils import simplejson

def dashboard(request):
    decks = Tag.objects.all()
    # do we need the RequestContext?
    return render_to_response('decks/dashboard.html',
                              {'decks' : decks},
                              context_instance=RequestContext(request))

def edit_card(request, deck_id, card_id=None):
    deck = get_object_or_404(Tag, pk=deck_id)

    if card_id is None:
        return render_to_response('decks/dashboard_editcard_block.html',
                                  {'deck' : deck},
                                  context_instance=RequestContext(request))
        #adding a new card

    card = get_object_or_404(Card, pk=card_id)
    if card.deck != deck:
        return HttpResponseBadRequest()

    return render_to_response('decks/dashboard_editcard_block.html',
                              {'card' : card, 'deck' : deck},
                              context_instance=RequestContext(request))


def view_deck(request, deck_id):
    deck = Tag.objects.get(pk=deck_id)
    if not deck.is_deck:  #TODO: do we care? change this method to view-tag?
        return HttpResponse(code=400)

    #cards = deck.deck_cards.all()
    cards = deck.deck_cards.filter(deleted=False)
    return render_to_response('decks/dashboard_viewdeck_block.html',
                              {'deck' : deck, 'cards' : cards})


def review_deck(request, deck_id):
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

    return render_to_response('decks/deckinfo_partial.html', {'deck' : deck})

def new_card(request, deck_id):
    if request.method != 'POST':
        return HttpResponseBadRequest()

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

    return HttpResponseRedirect(reverse('edit_new_card', kwargs={'deck_id' : deck_id}))

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

    return HttpResponse('success')


# vim: set ai et ts=4 sw=4 sts=4 :

