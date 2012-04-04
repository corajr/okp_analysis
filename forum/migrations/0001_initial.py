# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Author'
        db.create_table('forum_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('u_id', self.gf('django.db.models.fields.IntegerField')()),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('posts', self.gf('django.db.models.fields.IntegerField')()),
            ('okp_team', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('member_since', self.gf('django.db.models.fields.DateTimeField')()),
            ('profile_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('avatar_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('forum', ['Author'])

        # Adding model 'Message'
        db.create_table('forum_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mesg_id', self.gf('django.db.models.fields.IntegerField')()),
            ('mesg_num', self.gf('django.db.models.fields.IntegerField')()),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.Author'])),
            ('responding_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.Message'], null=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('signature', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('forum', ['Message'])

    def backwards(self, orm):
        # Deleting model 'Author'
        db.delete_table('forum_author')

        # Deleting model 'Message'
        db.delete_table('forum_message')

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
            'responding_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Message']", 'null': 'True'}),
            'signature': ('django.db.models.fields.TextField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['forum']