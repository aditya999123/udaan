# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from state_machine import ScreenStateMachine, SeatStateMachine
from udaan.Base import Base

from helper.checker import assert_found

class AddScreen(View):
	def __init__(self):
		self.ssm = ScreenStateMachine()

	def post(self, request, *args, **kwargs):
		newScreen = Base(request.data)

		assert_found(newScreen.name, "name not found")
		assert_found(newScreen.seatInfo, "seatinfo not found")

		response = self.ssm.addScreen(newScreen)
		return response

class ReserveTickets(View):
	def __init__(self):
		self.ssm = ScreenStateMachine()

	def post(self, request, *args, **kwargs):
		body = Base(request.data)

		body.screenName = kwargs.get('screenName', None)
		assert_found(body.seats, "seats detail not found")

		response = self.ssm.reserve(body)
		return response

class GetAvailableSeats(View):
	def __init__(self):
		self.ssm = ScreenStateMachine()

	def get(self, request, *args, **kwargs):
		body = Base(request.data)

		body.screenName = kwargs.get('screenName', None)

		if body.status:
			response = self.ssm.getSeats(body.screenName, body.status)
		elif body.numSeats != None and body.choice != None:
			response = self.ssm.getNearest(body.screenName, body.numSeats, body.choice)

		return response