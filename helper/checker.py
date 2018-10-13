from udaan.Base import Base

BAD_REQUEST = 502 # bad gateway ,server from another server
FORBIDDEN = 403 # permanent concrete error
NOT_FOUND = 404 # data / url not found
UNAUTHORIZED = 401 # retry on this error
SERVER_ERROR = 500 # internal server error


def build_body(message, status):
	response = Base()
	response.success = False

	if message is not None:
		response.message = message

	if status is not None:
		response.status = status

	return response

def assert_custom(condition, message = None, status = None):
	if condition == False:
		response = build_body(message, status)
		raise Exception(response)

def assert_valid(condition, message = None):
	assert_custom(condition, message, BAD_REQUEST)

def assert_allowed(condition, message = None):
	assert_custom(condition, message, FORBIDDEN)

def assert_authorized(condition, message = None):
	assert_custom(condition, message, UNAUTHORIZED)

def assert_found(obj, message = None):
	if obj is None:
		assert_custom(False, message, NOT_FOUND)
