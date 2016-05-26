# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'Match.winner' to match new field type.
        db.rename_column('tipping_match', 'winner_id', 'winner')
        # Changing field 'Match.winner'
        db.alter_column('tipping_match', 'winner', self.gf('django.db.models.fields.CharField')(max_length=4, null=True))

        # Removing index on 'Match', fields ['winner']
        #db.delete_index('tipping_match', ['winner_id'])


    def backwards(self, orm):

        # Adding index on 'Match', fields ['winner']
        db.create_index('tipping_match', ['winner_id'])

        # Renaming column for 'Match.winner' to match new field type.
        db.rename_column('tipping_match', 'winner', 'winner_id')
        # Changing field 'Match.winner'
        db.alter_column('tipping_match', 'winner_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tipping.Team'], null=True))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'tipping.competition': {
            'Meta': {'ordering': "('-start',)", 'object_name': 'Competition'},
            'clean_sweep_extra_points': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'end': ('django.db.models.fields.DateField', [], {}),
            'fee': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'season': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sport': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tipping.Sport']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        'tipping.match': {
            'Meta': {'ordering': "('round',)", 'object_name': 'Match'},
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_matches'", 'to': "orm['tipping.Team']"}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_matches'", 'to': "orm['tipping.Team']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kickoff': ('django.db.models.fields.DateTimeField', [], {}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matches'", 'to': "orm['tipping.Round']"}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matches'", 'to': "orm['tipping.Venue']"}),
            'winner': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        'tipping.registration': {
            'Meta': {'ordering': "('competition', 'user')", 'unique_together': "(('user', 'competition'),)", 'object_name': 'Registration'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'registrations'", 'to': "orm['tipping.Competition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'tipping.round': {
            'Meta': {'ordering': "('competition', 'start')", 'object_name': 'Round'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rounds'", 'to': "orm['tipping.Competition']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        'tipping.sport': {
            'Meta': {'ordering': "('description',)", 'object_name': 'Sport'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'tipping.team': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Team'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sport': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tipping.Sport']"})
        },
        'tipping.tip': {
            'Meta': {'ordering': "('match',)", 'unique_together': "(('registration', 'match'),)", 'object_name': 'Tip'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tips'", 'to': "orm['tipping.Match']"}),
            'registration': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tips'", 'to': "orm['tipping.Registration']"}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tips_to_win'", 'to': "orm['tipping.Team']"})
        },
        'tipping.venue': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Venue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sport': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tipping.Sport']"}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'home_grounds'", 'symmetrical': 'False', 'to': "orm['tipping.Team']"}),
            'used_in_competition': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['tipping']
