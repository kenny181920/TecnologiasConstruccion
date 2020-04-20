#!C:/Python3.8/python.exe

from flask import Flask
from flask_restful import Resource, Api, reqparse
import json

app = Flask(__name__)
api = Api(app)

ambitos = {}

ambitos.setdefault("cocina",["manzana","cuchara","platico","cebolla"])
ambitos.setdefault("limpieza",["escoba","trapeador","jabon", "cuchara"])
ambitos.setdefault("taller",["martillo","serrucho","desarmador"])

parser = reqparse.RequestParser()

class tipoProducto(Resource):
	def get(self):
		data = json.dumps(ambitos)
		return data

	def post(self):
		parser.add_argument("tipo")
		args = parser.parse_args()
		ambitos.setdefault(args["tipo"],[])
		return 201

class elementoProducto(Resource):
	def get(self):
		data = json.dumps(ambitos)
		return data

	def post(self):
		parser.add_argument("tipo")
		parser.add_argument("elemento")
		args = parser.parse_args()
		if args["tipo"] == "cocina":
			ambitos.setdefault("cocina", []).append(args["elemento"])
			return 201
		elif args["tipo"] == "limpieza":
			ambitos.setdefault("limpieza", []).append(args["elemento"])
			return 201
		elif args["tipo"] == "taller":
			ambitos.setdefault("taller", []).append(args["elemento"])
			return 201
		else:
			return "No se encuentra el ambito"

class busqueda(Resource):
    def get(self, producto_id):
    	resultado = []
    	for x in ambitos:
    		for y in ambitos[x]:
    			if y == producto_id:
    				resultado.append(x)
    	return json.dumps(resultado)

api.add_resource(tipoProducto, '/productos/')
api.add_resource(elementoProducto, '/elementos/')
api.add_resource(busqueda, '/busqueda/<producto_id>')

if __name__ == '__main__':
	app.run(debug=True)