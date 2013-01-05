from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Deck(MPTTModel):
    """
    Forms a DAG of decks and forks of that deck. This allows use us to combine stats
    determining number of times a deck was forked, etc. We can also use this to create
    a nice graph showing ancestors or children of a particular deck. Each time a person
    saves a deck to their profile, they're adding a new node to the DAG.

    A separate DAG models nested-deck relationships for a particular user's decks.
    """
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    tags = models.ManyToManyField(Tag, null=True)

    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)
    private = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    diff_from_parent = models.BooleanField(default=False)

    # the deck this deck was copied from
    parent = TreeForeignKey('self', null=True, blank=True, related_name='forks')

    # users can create nested decks
    super_deck = TreeForeignKey('self', null=True, blank=True, related_name='sub_decks')
    top_level = models.BooleanField(default=True)

    def card_count(self):
        return self.deck_cards.filter(active=True).count()

    def due_count(self):
        return self.deck_cards.filter(active=True, next_due__lt=timezone.now()).count()


class Card(models.Model):
    """
    A flash card.
    """
    deck = models.ForeignKey(Deck, related_name="deck_cards") # many to one
    front = models.TextField()
    back = models.TextField()

    last_asked = models.DateTimeField(null=True)
    next_due = models.DateTimeField(auto_now_add=True)

    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)
    active = models.BooleanField(default=True)
    private = models.BooleanField(default=False)

    def __unicode__(self):
        return "front: %s\nback: %s" % (self.front, self.back)

    def is_due(self):
        #return self.next_due < datetime.datetime.utcnow().replace(tzinfo=utc) <-- correct but long
        return self.next_due < timezone.now() and not self.deleted


# vim: set ai et ts=4 sw=4 sts=4 :
