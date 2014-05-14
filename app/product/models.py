from django.db import models

# Create your models here.

class Brand(models.Model):
	name = models.CharField(max_length=300)

class Appliance(models.Model):
	name = models.CharField(max_length=300)

class Product(models.Model):
	code = models.CharField(max_length=30)
	name = models.CharField(max_length=300)
	description = models.CharField(max_length=300)
	datetime = models.DateTimeField(auto_now=True)
	price = models.DecimalField(max_digits=9, decimal_places=2)
	ammount = models.IntegerField()
	brand = models.ForeignKey(Brand, null=False)
	appliance = models.ManyToManyField(Appliance)
	picture = models.ImageField(upload_to="pictures", null=True)


"""
>>> from django.core.files.base import ContentFile
>>> f=open('media/11451044.jpg', 'r')
>>> content = ContentFile(f.read())
>>> p.picture.save(f.name, content)

from django.core.files.base import ContentFile
def save_file(request):
	mymodel = MyModel.objects.get(id=1)
	file_content = ContentFile(request.FILES['video'].read())
	mymodel.video.save(request.FILES['video'].name, file_content)
	
"""