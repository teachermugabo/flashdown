from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from decks.models import Tag

def overview(request):
  decks = Tag.objects.all()
  # do we need the RequestContext?
  return render_to_response('decks/overview.html',
                            {'decks' : decks},
                            context_instance=RequestContext(request))

def edit_card(request, card_id):
  card = Tag.card_set.objects.get(pk=card_id)
  return render_to_response('decks/editcard.html', {'card' : card})

def new_card(request, deck_name):
  # TODO: combine with above?
  return render_to_response('decks/editcard.html')

# process an ajax request to add a new deck
def new_deck(request, deck_name):
  if not request.is_ajax():
    return HttpResponse(status=400)

  #TODO: validate data

  deck = None
  try:
    deck = Tag.objects.get(name=deck_name)
    return HttpResponse('')
  except Tag.DoesNotExist:
    deck = Tag(name=deck_name, is_deck=True)
    deck.save()

  return render_to_response('decks/deckinfo_partial.html', {'deck': deck})

def view_deck(request, deck_name):
  deck = Tag.objects.get(name=deck_name)
  if not deck.is_deck:  #TODO: do we care?
    return HttpResponse(code=400)

  cards = deck.deck_cards.all()
  return render_to_response('decks/viewdeck.html', {'deck' : deck, 'cards' : cards})

def review_deck(request, deck_name):
  return render_to_response('decks/reviewdeck.html')

