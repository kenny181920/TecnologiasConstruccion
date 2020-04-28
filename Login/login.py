from flask import Flask
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
api = Api(app, prefix="/login")
auth = HTTPBasicAuth()

Data_Usuario = {
	"kenny": "123456"
}

@auth.verify_password
def verify(username, password):
	if not(username and password):
		return False
	return Data_Usuario.get(username) == password

class PrivateResource(Resource):
	@auth.login_required
	def get(self):
		return "Login Exitoso"

api.add_resource(PrivateResource, '/private')

if __name__ == '__main__':
	app.run(debug=True)
