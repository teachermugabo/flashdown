from django.db import models
#from django.utils import timezone
from django.utils import timezone #

class Tag(models.Model):
    name = models.CharField(max_length=50)
    is_deck = models.BooleanField(default=False) # for filtering purposes
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def card_count(self):
        return self.deck_cards.filter(deleted=False).count()

    def due_count(self):
        return self.deck_cards.filter(deleted=False, next_due__lt=timezone.now()).count()

class Card(models.Model):
    front = models.TextField()
    back = models.TextField()
    deck = models.ForeignKey(Tag, related_name="deck_cards") # one to many
    tags = models.ManyToManyField(Tag, related_name="tagged_cards") # many to many
    deleted = models.BooleanField(default=False)

    last_asked = models.DateTimeField(null=True)
    next_due = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.front + "\n" + self.back

    def is_due(self):
        #return self.next_due < datetime.datetime.utcnow().replace(tzinfo=utc) <-- correct but long
        return self.next_due < timezone.now() and not self.deleted


# vim: set ai et ts=4 sw=4 sts=4 :
