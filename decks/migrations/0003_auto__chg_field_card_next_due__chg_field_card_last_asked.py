# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Card.next_due'
        db.alter_column('decks_card', 'next_due', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'Card.last_asked'
        db.alter_column('decks_card', 'last_asked', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'Card.next_due'
        db.alter_column('decks_card', 'next_due', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Card.last_asked'
        db.alter_column('decks_card', 'last_asked', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 10, 14, 0, 0)))

    models = {
        'decks.card': {
            'Meta': {'object_name': 'Card'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deck': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deck_cards'", 'to': "orm['decks.Tag']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_asked': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'next_due': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tagged_cards'", 'symmetrical': 'False', 'to': "orm['decks.Tag']"})
        },
        'decks.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deck': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['decks']