from django.http import JsonResponse
from udaan.Base import Base
import json
from exceptions import RuntimeError

class Watcher:
	def __init__(self, get_response):
		self.get_response = get_response
		# One-time configuration and initialization.

	def __call__(self, request):
		methods = ['GET', 'POST']
		if request.method in methods:
			try:
				body = json.loads(request.body)
			except:
				body = {key: value for (key, value) in (request.GET.items() + request.POST.items())}
		
			request.data = body
			response = self.get_response(request)
		elif request.method == 'OPTIONS':
			response = Base()
			response.message = "options method"
		else:
			response = Base()
			response.status = 404
			response.message = "Method not found"
			response.success = False
		
		# print response
		if isinstance(response, Base):
			response = JsonResponse(response.toJSON(), status = response.status)
		
		headers = {
			'Access-Control-Allow-Origin' : '*',
			'Access-Control-Allow-Headers' : '*',
			'Access-Control-Allow-Methods' : '*'
			}

		for header, value in headers.iteritems():
			response[header] = value

		return response

	def process_exception(self, request, exception):
		response = Base()
		
		message = """\nException :\n##########################\n%s\n######################\n"""

		if isinstance(exception.message, Base):
			response = exception.message
			print "20000000000"
			print message%(response.toJSON())
		else:
			response.success = False
			print "500"
			response.message = "internal server error :%s"%(exception)
			response.status = 500
			print message%(exception)

		response = JsonResponse(response.toJSON(), status = response.status)  
		return response