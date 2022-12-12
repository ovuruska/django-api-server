from django.db import models

from ..common import BaseModel


class Branch(BaseModel):
	name = models.CharField(max_length=256)
	address = models.CharField(max_length=256)
	description = models.CharField(max_length=256,default="")
	tubs = models.IntegerField()


	class Meta:
		...