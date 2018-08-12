# POST METHOD IS EXPECTED
from app import VRPService
import json

def application(env, start_response):
	start_response('200 OK', [('Content-Type', 'text/json')])
	try:
		request_body_size = int(env.get('CONTENT-LENGTH', 0))
	except:
		request_body_size = 0

	if env['REQUEST_METHOD'] == "POST" and env.get("CONTENT_TYPE", "application/json"):
		request_body = env['wsgi.input'].read(request_body_size)
		data = json.loads(request_body.decode())
		response = VRPService(data).get_response()
	else:
		response = {
			"status": "METHOD_NOT_ALLOWED",
			"message": "method not allow or json expected but not found"
		}

	return bytes(json.dumps(response), "utf-8")
