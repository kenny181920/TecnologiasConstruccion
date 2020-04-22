import http.client

file = open('palabras.txt', 'r')
file_r = open('resultados.txt','w')  

api = http.client.HTTPSConnection("linguatools-conjugations.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "linguatools-conjugations.p.rapidapi.com",
    'x-rapidapi-key': "961105f553msh1e8effe69ef2988p11f182jsn1f28601f3fb3"
    }

c1 = "/conjugate/?verb="

for x in file:
	consulta = (c1 + x)[:-1]
	api.request("GET", consulta, headers=headers)
	res = api.getresponse()
	data = res.read()
	#print(data)
	data2 = str(data)
	file_r.write(data2)
file_r.close()