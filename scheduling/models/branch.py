from django.db import models

from common import BaseModel


class Branch(BaseModel):
	name = models.CharField(max_length=256,default="",blank=True)
	address = models.CharField(max_length=256,default="",blank=True)
	description = models.CharField(max_length=256,default="",blank=True)
	phone = models.CharField(max_length=32,default="",blank=True)
	email = models.EmailField(default="",blank=True)
	tubs = models.IntegerField(default=0,blank=True)

	class Meta:
		...