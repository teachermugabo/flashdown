# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Rename question & answer to front & back
        db.rename_column('decks_card', 'question', 'front')
        db.rename_column('decks_card', 'answer', 'back')


    def backwards(self, orm):
        db.rename_column('decks_card', 'front', 'question')
        db.rename_column('decks_card', 'back', 'answer')


    models = {
        'decks.card': {
            'Meta': {'object_name': 'Card'},
            'back': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deck': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deck_cards'", 'to': "orm['decks.Tag']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_asked': ('django.db.models.fields.DateTimeField', [], {}),
            'next_due': ('django.db.models.fields.DateTimeField', [], {}),
            'front': ('django.db.models.fields.TextField', [], {}),
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
