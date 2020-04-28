from flask import Flask, jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import json
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678'

data_usuarios = {
    "kenny": generate_password_hash("12345678")
}

with open('paises.json') as f:
	data_pais = json.load(f)

def actualizarFichero(data):
	with open('paises.json', 'w') as file:
		json.dump(data,file)

def toke_requerid(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = request.args.get('token')
		if not token:
			return jsonify({'mensaje' : 'Falta el token'}), 403
		try:
			data = jwt.decode(token, app.config['SECRET_KEY'])
		except:
			return jsonify({'mensaje' : 'Token invalido'}), 403
		return f(*args, **kwargs)
	return decorated

@app.route('/pais', methods=['GET'])
@toke_requerid
def mostrarPaises():
	data = []
	for x in data_pais:
 		data.append(x)
	return jsonify(data)

@app.route('/pais', methods=['POST'])
@toke_requerid
def agregarPais():
	pais = request.args.get('pais')
	data_pais.update({pais : {}})
	actualizarFichero(data_pais)
	return jsonify(data_pais)

@app.route('/region', methods=['POST'])
@toke_requerid
def agregarRegion():
	pais = request.args.get('pais')
	region = request.args.get('region')
	if data_pais[pais]:
		data_pais[pais].update({region:{}})
		actualizarFichero(data_pais)
		return jsonify(data_pais)
	else:
		return jsonify({'mensaje' : 'No existe la region'}), 403

@app.route('/distrito', methods=['POST'])
@toke_requerid
def agregarDistrito():
	pais = request.args.get('pais')
	region = request.args.get('region')
	distrito = request.args.get('distrito')
	if (data_pais[pais][region] == {}) or data_pais[pais][region]:
		data_pais[pais][region].update({ distrito : {}})
		actualizarFichero(data_pais)
		return jsonify(data_pais)
	else:
		return jsonify({'mensaje' : 'No existe el distrito'}), 403

@app.route('/pais', methods=['PUT'])
@toke_requerid
def actualizarPais():
	pais = request.args.get('pais')
	paisActualido = request.args.get('paisActualido')
	if data_pais[pais]:
		data_pais[paisActualido] = data_pais.pop(pais)
		actualizarFichero(data_pais)
		return jsonify(data_pais)
	else:
		return jsonify({'mensaje' : 'No existe el pais'}), 403

@app.route('/pais', methods=['DELETE'])
@toke_requerid
def quitarPais():
	pais = request.args.get('pais')
	if pais in data_pais:
		del data_pais[pais]
		actualizarFichero(data_pais)
		return jsonify(data_pais)
	else:
		return jsonify({'mensaje' : 'No existe el pais'}), 403

@app.route('/login')
def login():
	auth = request.authorization
	if auth and (auth.username in data_usuarios) and check_password_hash(data_usuarios.get(auth.username), auth.password):
		token = jwt.encode({'user':auth.username, 'exp':datetime.datetime.utcnow() +datetime.timedelta(minutes=5) },app.config['SECRET_KEY'])
		return jsonify({'token':token.decode('UTF-8')})
	return make_response('Could not verify!',401,{'WWW-Authenticate':'Basic realm="Login Required"'})

if __name__ == '__main__':
	app.run(debug=True)