# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Rename field 'Message.responding_to'
        db.rename_column('forum_message', 'responding_to_id', 'parent_id')

        # Alter field 'Message.parent'
        db.alter_column('forum_message', 'parent',
             models.ForeignKey(orm['forum.Message'], related_name='children_set', null=True))

    def backwards(self, orm):
        # Adding field 'Message.responding_to'
        db.add_column('forum_message', 'responding_to',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.Message'], null=True),
                      keep_default=False)

        # Deleting field 'Message.parent'
        db.delete_column('forum_message', 'parent_id')

    models = {
        'forum.author': {
            'Meta': {'object_name': 'Author'},
            'avatar_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member_since': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'okp_team': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'posts': ('django.db.models.fields.IntegerField', [], {}),
            'profile_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'u_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'forum.message': {
            'Meta': {'object_name': 'Message'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Author']"}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mesg_id': ('django.db.models.fields.IntegerField', [], {}),
            'mesg_num': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children_set'", 'null': 'True', 'to': "orm['forum.Message']"}),
            'signature': ('django.db.models.fields.TextField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['forum']
