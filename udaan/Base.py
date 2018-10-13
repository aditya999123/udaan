from django.db.models import Model
from helper.serializer import get_json_serializable
import json

class Base:
	def __init__(self, obj = None):
		self.success = True
		self.message = "Your message goes here"
		self.status = 200

		if obj is not None:
			if isinstance(obj, Model):
				self.__dict__ = get_json_serializable(obj)

			if isinstance(obj, dict):
				self.__dict__ = obj


	def __getattr__(self, item):
		return self.__dict__.get(item, None)
		# return None

	def __repr__(self):
		return self.__dict__.__str__()


	def toJSON(self, basic = True):
		response = {}
		exclude = ['success', 'status', 'message']
		for key, val in self.__dict__.iteritems():
			if basic == False and key in exclude:
				continue
			if isinstance(val, Base):
				# continue
				val = val.toJSON(False)
			if isinstance(val, list):
				data = []
				for item in val:
					if isinstance(item, Base):
						data.append(item.toJSON(False))
					else:
						data.append(item)
				val = data
			response[key] = val
		return response

	# def load(self, data):
	# 	if data is None:
	# 		return
		
	# 	keys = self.__dict__.keys()
	# 	if isinstance(data, unicode):
	# 		data = json.loads(data)

	# 	#exclude overriding
	# 	exclude = ['success', 'status', 'message']
	# 	for excl in exclude:
	# 		keys.remove(excl)

