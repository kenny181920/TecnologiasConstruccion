#!C:/Python3.8/python.exe

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

ambitos = {}

ambitos.setdefault("cocina",["manzana","cuchara","platico","cebolla"])
ambitos.setdefault("limpieza",["escoba","trapeador","jabon", "cuchara"])
ambitos.setdefault("taller",["martillo","serrucho","desarmador"])

parser = reqparse.RequestParser()

@app.route('/productos', methods=['GET'])
def listaGeneral():
	return jsonify(ambitos)

@app.route('/productos', methods=['POST'])
def agregarProducto():
	tipo = request.args.get('tipo')
	ambitos.setdefault(tipo,[])
	return jsonify(201)

@app.route('/elementos', methods=['POST'])
def agregarElementos():
	tipo = request.args.get('tipo')
	elemento = request.args.get('elemento')
	if tipo == "cocina":
		ambitos.setdefault("cocina", []).append(elemento)
		return jsonify(201)
	elif tipo == "limpieza":
		ambitos.setdefault("limpieza", []).append(elemento)
		return jsonify(201)
	elif tipo == "taller":
		ambitos.setdefault("taller", []).append(elemento)
		return jsonify(201)
	else:
		return jsonify('No se encuentra el ambito')

@app.route('/elementos', methods=['PUT'])
def actualizarElemento():
	tipo = request.args.get('tipo')
	elemento = request.args.get('elemento')
	ACelemento = request.args.get('ACelemento')
	if (tipo in ambitos) and (elemento in ambitos[tipo]):
		for x in range(len(ambitos[tipo])):
			if ambitos[tipo][x] == elemento:
				ambitos[tipo][x] = ACelemento
		return jsonify('Actualizado')
	else:
		return jsonify('No encontrado')

@app.route('/elementos', methods=['DELETE'])
def eliminarElemento():
	tipo = request.args.get('tipo')
	elemento = request.args.get('elemento')
	if (tipo in ambitos) and (elemento in ambitos[tipo]):
		ambitos[tipo].remove(elemento)
		return jsonify('Eliminado')
	else:
		return jsonify('No encontrado')

@app.route('/elementos/busqueda', methods=['GET'])
def busquedaElementos():
	elemento = request.args.get('elemento')
	resultado = []
	for x in ambitos:
		for y in ambitos[x]:
			if y == elemento:
				resultado.append(x)
	return jsonify(resultado)



if __name__ == '__main__':
	app.run(debug=True)