from models import Screen, Row, Seat
from udaan.Base import Base

from helper.methods import get_or_none
from helper.checker import assert_allowed, assert_found


class ScreenStateMachine():
	def __init__(self):
		self.rsm = RowStateMachine()

	def addScreen(self, newScreen):
		screen = Screen.objects.create(name = newScreen.name)
		for rowName, details in newScreen.seatInfo.items():
			newRow = Base(details)
			newRow.name = rowName
			newRow.screen = screen
			self.rsm.addRow(newRow)
		return Base(screen)

	def reserve(self, body):
		screen = get_or_none(Screen, name = body.screenName)
		assert_found(screen)
		return self.rsm.reserve(screen, body.seats)

	def getSeats(self, screenName, status):
		screen = get_or_none(Screen, name = screenName)
		assert_found(screen)

		return self.rsm.getSeats(screen, status)

class RowStateMachine():
	def __init__(self):
		self.seatsm = SeatStateMachine()

	def addRow(self, newRow):
		row = Row.objects.create(
			screen = newRow.screen,
			name = newRow.name,
			numberOfSeats = newRow.numberOfSeats
		)
		newSeats = Base()
		newSeats.row = row
		newSeats.aisleSeats = newRow.aisleSeats
		self.seatsm.addSeats(newSeats)

		return row

	def reserve(self, screen, seats):
		seatsToReserve = []
		for rowName in seats.keys():
			row = get_or_none(Row, name = rowName, screen = screen)
			assert_found(row)
			for seat in seats[rowName]:
				seatToReserve = Base()
				seatToReserve.number = seat
				seatToReserve.row = row

				seatsToReserve.append(seatToReserve)

		return self.seatsm.reserve(seatsToReserve)

	def getSeats(self, screen, status):
		response = Base()
		response.seats = []
		for row in Row.objects.filter(screen = screen):
			seats = self.seatsm.getSeats(row, status)
			for seat in seats:
				response.seats.append(Base(seat))

		return response

class SeatStateMachine():
	def __init__(self):
		pass

	def getSeats(self, row, status):
		reserved = not(status == 'unreserved')

		seats = []

		for seat in Seat.objects.filter(row=row, isReserved = reserved):
			seats.append(seat)

		return seats

	def addSeats(self, newSeats):
		numberOfSeats = newSeats.row.numberOfSeats
		aisleSeats = newSeats.aisleSeats
		row = newSeats.row
		seats = []

		for i in range(0, numberOfSeats):
			seat = Seat.objects.create(
				row = row,
				number = i,
				isAisle = (i in aisleSeats)
			)

			seats.append(seat)

		return seats

	def reserve(self, seatsToReserve):
		possible = True

		for seat in seatsToReserve:
			seatObj = get_or_none(Seat,				
				row = seat.row,
				number = seat.number	
			)

			assert_found(seatObj)

			if seatObj.isReserved :
				possible = False
				break

		assert_allowed(possible, "already booked")
	
		seatsReserved = []

		for seat in seatsToReserve:
			seatObj = Seat.objects.get(
				row = seat.row,
				number = seat.number
			)

			seatObj.isReserved = True
			seatObj.save()

			seatsReserved.append(Base(seatObj))

		response = Base()
		response.seatsReserved = seatsReserved

		return response