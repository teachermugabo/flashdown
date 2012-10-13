from django.conf.urls import patterns, url

urlpatterns = patterns('decks.views',
    url(r'^/?$', 'overview', name='overview'),
    # we edit/add a single card at a time
    url(r'^edit/(?P<card_id>\w+)/$', 'edit_card', name='edit_card'),
    url(r'^(?P<deck_name>\w+)/new-card/$', 'new_card', name='new_card'),
    # view a list of all cards in a deck
    url(r'^view/(?P<deck_name>\w+)/$', 'view_deck', name='view_deck'),
    # we review an entire deck (deck data passed to template all at once)
    url(r'^review/(?P<deck_name>\w+)/$', 'review_deck', name='review_deck'),
    # add a new deck (ajax)
    url(r'^new-deck/(?P<deck_name>[a-zA-z_0-9-%]+)/$', 'new_deck', name='new_deck'),
)
