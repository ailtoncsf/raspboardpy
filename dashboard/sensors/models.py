from __future__ import unicode_literals

from django.core import serializers
from django.db import models

# Create your models here.
from django.utils import timezone

class Log(models.Model):   
    variavel = models.CharField(max_length=200)
    unidade = models.CharField(max_length=10)
    valor = models.FloatField()
    data = models.DateTimeField(
            default=timezone.now)

    def gravar(self):
        self.data = timezone.now()
        self.save()

    def __str__(self):
    	# assuming obj is a model instance
		serialized = serializers.serialize('json', [ self, ])
		return serialized
        #return dict(
        #    input_variavel=self.variavel, 
        #    input_unidade=self.unidade,
        #    input_valor=self.valor, 
        #    input_data=self.data.isoformat())		

