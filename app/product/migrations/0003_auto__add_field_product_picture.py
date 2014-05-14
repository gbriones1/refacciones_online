# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Product.picture'
        db.add_column(u'product_product', 'picture',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Product.picture'
        db.delete_column(u'product_product', 'picture')


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
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'})
        }
    }

    complete_apps = ['product']