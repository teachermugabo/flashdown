from django.conf.urls import patterns, url

urlpatterns = patterns('decks.views',
    url(r'^/?$', 'dashboard', name='dashboard'),
    # we edit/add a single card at a time
    url(r'^(?P<deck_id>\d+)/edit-card/$', 'edit_card', name='edit_new_card'),
    url(r'^(?P<deck_id>\d+)/edit-card/(?P<card_id>\d+)/$', 'edit_card', name='edit_card'),

    # view a list of all cards in a deck
    url(r'^(?P<deck_id>\d+)/view/$', 'view_deck', name='view_deck'),
    # we review an entire deck (deck data passed to template all at once)
    url(r'^(?P<deck_id>\d+)/review/$', 'review_deck', name='review_deck'),

    # add a new deck (ajax)
    url(r'^new-deck/$', 'new_deck', name='new_deck'),
    # add a new card (ajax)
    url(r'^(?P<deck_id>\d+)/new-card/$', 'new_card', name='new_card'),
    # delete a card (ajax)
    url(r'^(?P<deck_id>\d+)/delete-card/(?P<card_id>\d+)/$', 'delete_card', name='delete_card'),
)
