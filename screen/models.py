# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Screen(models.Model):
	name = models.CharField(max_length = 120, blank = False, null = False)
	modified = models.DateTimeField(auto_now = True, auto_now_add = False)
	created = models.DateTimeField(auto_now = False, auto_now_add = True)


class Row(models.Model):
	screen = models.ForeignKey(Screen)
	name = models.CharField(max_length = 120, blank = False, null = False)
	numberOfSeats = models.IntegerField(default = 1)
	modified = models.DateTimeField(auto_now = True, auto_now_add = False)
	created = models.DateTimeField(auto_now = False, auto_now_add = True)


class Seat(models.Model):
	row = models.ForeignKey(Row)
	number = models.IntegerField(default = 0)
	isReserved = models.BooleanField(default = False)
	isAisle = models.BooleanField(default = False)
	modified = models.DateTimeField(auto_now = True, auto_now_add = False)
	created = models.DateTimeField(auto_now = False, auto_now_add = True)
