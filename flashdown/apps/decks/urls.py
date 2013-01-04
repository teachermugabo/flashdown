from django.conf.urls import patterns, url

urlpatterns = patterns('apps.decks.views',
    url(r'^/?$', 'overview', name='overview'),

    # open editor for a new card (optionally specify the deck)
    url(r'^add-cards/$', 'add_cards', name='add_cards'),
    url(r'^(?P<deck_id>\d+)/add-cards/$', 'add_cards', name='add_cards_to_deck'),

    # view a list of all cards in a deck
    url(r'^browse/$', 'browse', name='browse_all'),
    url(r'^(?P<deck_id>\d+)/browse/$', 'browse', name='browse'),

    # we review an entire deck (deck data passed to template all at once)
    url(r'^(?P<deck_id>\d+)/review/$', 'review', name='review'),

    ################################
    # AJAX urls                    #
    ################################

    # get a list of cards for a deck id (ajax)
    url(r'^(?P<deck_id>\d+)/get-cards/$', 'get_cards', name='get_cards'),

    # add a new deck (ajax)
    url(r'^new-deck/$', 'new_deck', name='new_deck'),

    # delete a deck (ajax)
    url(r'^(?P<deck_id>\d+)/delete-deck/$', 'delete_deck', name='delete_deck'),

    # add a new card (ajax)
    url(r'^new-card/$', 'new_card', name='new_card'),

    # update card data (ajax)
    url(r'^update-card/$', 'update_card', name='update_card'),

    # delete a card (ajax)
    url(r'^(?P<deck_id>\d+)/delete-card/(?P<card_id>\d+)/$', 'delete_card', name='delete_card'),
)
