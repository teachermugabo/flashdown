from django.db import models
#from django.utils import timezone
import datetime

class Tag(models.Model):
  name = models.CharField(max_length=50, unique=True)
  is_deck = models.BooleanField(default=False) # for filtering purposes

  def __unicode__(self):
    return self.name

class Card(models.Model):
  front = models.TextField()
  back = models.TextField()
  deck = models.ForeignKey(Tag, related_name="deck_cards") # one to many
  tags = models.ManyToManyField(Tag, related_name="tagged_cards") # many to many

  last_asked = models.DateTimeField(null=True)
  next_due = models.DateTimeField(auto_now_add=True)
  created = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return self.question + "\n\n" + self.answer

  def is_due(self):
    return self.next_due > datetime.now()


