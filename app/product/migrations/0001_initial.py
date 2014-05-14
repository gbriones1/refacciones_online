# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Brand'
        db.create_table(u'product_brand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'product', ['Brand'])

        # Adding model 'Appliance'
        db.create_table(u'product_appliance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'product', ['Appliance'])

        # Adding model 'Product'
        db.create_table(u'product_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
            ('ammount', self.gf('django.db.models.fields.IntegerField')()),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['product.Brand'])),
        ))
        db.send_create_signal(u'product', ['Product'])

        # Adding M2M table for field appliance on 'Product'
        m2m_table_name = db.shorten_name(u'product_product_appliance')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm[u'product.product'], null=False)),
            ('appliance', models.ForeignKey(orm[u'product.appliance'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'appliance_id'])


    def backwards(self, orm):
        # Deleting model 'Brand'
        db.delete_table(u'product_brand')

        # Deleting model 'Appliance'
        db.delete_table(u'product_appliance')

        # Deleting model 'Product'
        db.delete_table(u'product_product')

        # Removing M2M table for field appliance on 'Product'
        db.delete_table(db.shorten_name(u'product_product_appliance'))


    models = {
        u'product.appliance': {
            'Meta': {'object_name': 'Appliance'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'product.brand': {
            'Meta': {'object_name': 'Brand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'product.product': {
            'Meta': {'object_name': 'Product'},
            'ammount': ('django.db.models.fields.IntegerField', [], {}),
            'appliance': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['product.Appliance']", 'symmetrical': 'False'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['product.Brand']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'price': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['product']