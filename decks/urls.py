from django.conf.urls import patterns, url

urlpatterns = patterns('decks.views',
    url(r'^/?$', 'overview', name='overview'),
    # we edit/add a single card at a time
    url(r'^(?P<deck_id>\w)/edit-card/$', 'edit_card', name='edit_new_card'),
    url(r'^(?P<deck_id>\w)/edit-card/(?P<card_id>\w+)/$', 'edit_card', name='edit_card'),

    # view a list of all cards in a deck
    url(r'^(?P<deck_id>\w)/view/$', 'view_deck', name='view_deck'),
    # we review an entire deck (deck data passed to template all at once)
    url(r'^(?P<deck_id>\w)/review/$', 'review_deck', name='review_deck'),

    # add a new deck (ajax)
    url(r'^new-deck/$', 'new_deck', name='new_deck'),
    # add a new card (ajax)
    url(r'^(?P<deck_id>\w)/new-card/$', 'new_card', name='new_card'),
)
