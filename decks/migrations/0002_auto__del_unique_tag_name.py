# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Tag', fields ['name']
        db.delete_unique('decks_tag', ['name'])


    def backwards(self, orm):
        # Adding unique constraint on 'Tag', fields ['name']
        db.create_unique('decks_tag', ['name'])


    models = {
        'decks.card': {
            'Meta': {'object_name': 'Card'},
            'back': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deck': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deck_cards'", 'to': "orm['decks.Tag']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'front': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_asked': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'next_due': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tagged_cards'", 'symmetrical': 'False', 'to': "orm['decks.Tag']"})
        },
        'decks.tag': {
            'Meta': {'object_name': 'Tag'},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deck': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['decks']