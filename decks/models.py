from django.db import models
from django.utils import timezone
import datetime

class Tag(models.Model):
  name = models.CharField(max_length=50, unique=True)
  is_deck = models.BooleanField(default=False) # for filtering purposes

  def __unicode__(self):
    return self.name

class Card(models.Model):
  question = models.TextField()
  answer = models.TextField()
  tags = models.ManyToManyField(Tag, related_name="tagged_cards") # many to many
  deck = models.ForeignKey(Tag, related_name="deck_cards") # one to many
  last_asked = models.DateTimeField()
  next_due = models.DateTimeField()

  def __unicode__(self):
    return self.question + "\n\n" + self.answer

  def is_due(self):
    return self.next_due > datetime.now()


