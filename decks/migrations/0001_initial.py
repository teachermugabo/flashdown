# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table('decks_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('is_deck', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('decks', ['Tag'])

        # Adding model 'Card'
        db.create_table('decks_card', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('front', self.gf('django.db.models.fields.TextField')()),
            ('back', self.gf('django.db.models.fields.TextField')()),
            ('deck', self.gf('django.db.models.fields.related.ForeignKey')(related_name='deck_cards', to=orm['decks.Tag'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_asked', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('next_due', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('decks', ['Card'])

        # Adding M2M table for field tags on 'Card'
        db.create_table('decks_card_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('card', models.ForeignKey(orm['decks.card'], null=False)),
            ('tag', models.ForeignKey(orm['decks.tag'], null=False))
        ))
        db.create_unique('decks_card_tags', ['card_id', 'tag_id'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table('decks_tag')

        # Deleting model 'Card'
        db.delete_table('decks_card')

        # Removing M2M table for field tags on 'Card'
        db.delete_table('decks_card_tags')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deck': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['decks']
