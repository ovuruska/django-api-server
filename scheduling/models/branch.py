from django.db import models

from ..common import BaseModel


class Branch(BaseModel):
	name = models.CharField(max_length=256,default="")
	address = models.CharField(max_length=256,default="")
	description = models.CharField(max_length=256,default="")
	phone = models.CharField(max_length=32,default="")
	email = models.EmailField(default="")

	class Meta:
		...