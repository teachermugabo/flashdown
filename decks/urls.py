from django.conf.urls import patterns, url

urlpatterns = patterns('decks.views',
    url(r'^/?$', 'overview', name='overview'),

    # open editor for a new card (optionally specify the deck)
    url(r'^add-cards/$', 'add_cards', name='add_cards'),
    url(r'^(?P<deck_id>\d+)/add-cards/$', 'add_cards', name='add_cards_to_deck'),

    # view a list of all cards in a deck
    url(r'^(?P<deck_id>\d+)/browse/$', 'browse', name='browse'),

    # we review an entire deck (deck data passed to template all at once)
    url(r'^(?P<deck_id>\d+)/review/$', 'review', name='review'),


    # update card data (ajax)
    url(r'^update-card/(?P<card_id>\d+)$', 'update_card', name='update_card'),

    # add a new card (ajax)
    url(r'^new-card/$', 'new_card', name='new_card'),

    # add a new deck (ajax)
    url(r'^new-deck/$', 'new_deck', name='new_deck'),
    # delete a card (ajax)
    url(r'^(?P<deck_id>\d+)/delete-card/(?P<card_id>\d+)/$', 'delete_card', name='delete_card'),
)
