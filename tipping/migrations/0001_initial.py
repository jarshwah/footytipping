# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Sport'
        db.create_table('tipping_sport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('tipping', ['Sport'])

        # Adding model 'Team'
        db.create_table('tipping_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sport', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tipping.Sport'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('tipping', ['Team'])

        # Adding model 'Venue'
        db.create_table('tipping_venue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sport', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tipping.Sport'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('used_in_competition', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('tipping', ['Venue'])

        # Adding M2M table for field teams on 'Venue'
        db.create_table('tipping_venue_teams', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('venue', models.ForeignKey(orm['tipping.venue'], null=False)),
            ('team', models.ForeignKey(orm['tipping.team'], null=False))
        ))
        db.create_unique('tipping_venue_teams', ['venue_id', 'team_id'])

        # Adding model 'Competition'
        db.create_table('tipping_competition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sport', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tipping.Sport'])),
            ('season', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
            ('fee', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=7, decimal_places=2)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('tipping', ['Competition'])

        # Adding model 'Round'
        db.create_table('tipping_round', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rounds', to=orm['tipping.Competition'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('tipping', ['Round'])

        # Adding model 'Match'
        db.create_table('tipping_match', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('round', self.gf('django.db.models.fields.related.ForeignKey')(related_name='matches', to=orm['tipping.Round'])),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='matches', to=orm['tipping.Venue'])),
            ('home_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='home_matches', to=orm['tipping.Team'])),
            ('away_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='away_matches', to=orm['tipping.Team'])),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tipping.Team'])),
        ))
        db.send_create_signal('tipping', ['Match'])

        # Adding model 'Registration'
        db.create_table('tipping_registration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tipping.Competition'])),
            ('paid', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('tipping', ['Registration'])

        # Adding model 'Tip'
        db.create_table('tipping_tip', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('registration', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tipping.Registration'])),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tipping.Match'])),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tipping.Team'])),
        ))
        db.send_create_signal('tipping', ['Tip'])


    def backwards(self, orm):

        # Deleting model 'Sport'
        db.delete_table('tipping_sport')

        # Deleting model 'Team'
        db.delete_table('tipping_team')

        # Deleting model 'Venue'
        db.delete_table('tipping_venue')

        # Removing M2M table for field teams on 'Venue'
        db.delete_table('tipping_venue_teams')

        # Deleting model 'Competition'
        db.delete_table('tipping_competition')

        # Deleting model 'Round'
        db.delete_table('tipping_round')

        # Deleting model 'Match'
        db.delete_table('tipping_match')

        # Deleting model 'Registration'
        db.delete_table('tipping_registration')

        # Deleting model 'Tip'
        db.delete_table('tipping_tip')


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
            'Meta': {'object_name': 'Competition'},
            'end': ('django.db.models.fields.DateField', [], {}),
            'fee': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'season': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sport': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tipping.Sport']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        'tipping.match': {
            'Meta': {'object_name': 'Match'},
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_matches'", 'to': "orm['tipping.Team']"}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_matches'", 'to': "orm['tipping.Team']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matches'", 'to': "orm['tipping.Round']"}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matches'", 'to': "orm['tipping.Venue']"}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tipping.Team']"})
        },
        'tipping.registration': {
            'Meta': {'object_name': 'Registration'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tipping.Competition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'tipping.round': {
            'Meta': {'object_name': 'Round'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rounds'", 'to': "orm['tipping.Competition']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        'tipping.sport': {
            'Meta': {'object_name': 'Sport'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'tipping.team': {
            'Meta': {'object_name': 'Team'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sport': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tipping.Sport']"})
        },
        'tipping.tip': {
            'Meta': {'object_name': 'Tip'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tipping.Match']"}),
            'registration': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tipping.Registration']"}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tipping.Team']"})
        },
        'tipping.venue': {
            'Meta': {'object_name': 'Venue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sport': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tipping.Sport']"}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'home_grounds'", 'symmetrical': 'False', 'to': "orm['tipping.Team']"}),
            'used_in_competition': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['tipping']
