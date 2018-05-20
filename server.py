import http.server
import random
import time
"""NE PAS OUBLIER DE LANCER LE SCRIPT QUI GENERE LES VALEURS DANS LES FICHIERS -___- """
FILE = 'visu.html'
PORT = 8000

nb_features = 22

class TestHandler(http.server.SimpleHTTPRequestHandler):
	"""The test example handler."""

	def do_POST(self):
		"""Handle a post request by returning the square of the number."""
		print(self.headers)
		length = int(self.headers.get_all('content-length')[0])
		print(self.headers.get_all('content-length'))
		data_string = (self.rfile.read(length)).decode("utf-8")
		print(data_string)
		tab = charge_fichier()
		print(tab)
		"""print(tab)"""
		self.send_response(200)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
		self.flush_headers()
		json = createJson(tab,data_string)			
		self.wfile.write(str(json).encode())

def createJson(tab, data):
	index = -1
	nb_bande = -1
	if(data == "400-500"):
		index = 0
		nb_bande = 1
	elif(data == "800-900"):
		index = 1
		nb_bande = 1
	elif(data == "2400-2500"):
		index = 2
		nb_bande = 1
	elif(data == "WiFi"):
		index = 19
		nb_bande = 3
	elif(data == "ZigBee"):
		index = 3
		nb_bande = 8
	elif(data == "Bluetooth/BLE"):
		index = 4
		nb_bande = 8

	json = '{"nbtab":'+str(nb_bande)+', "tabs":['

	for i in range(nb_bande):
		val_max = abs(round(float(tab[index][1]),2))
		val_min = abs(round(float(tab[index][2]),2))
		val_mean = abs(round(float(tab[index][3]),2))
		val_median = abs(round(float(tab[index][4]),2))
		val_std = abs(round(float(tab[index][5]),2))
		val_sum = abs(round(float(tab[index][6]),2)/1000000)
		json = json + '['+str(val_max) +','+str(val_min)+','+str(val_mean)+','+str(val_median)+','+str(val_std)+','+str(val_sum)+']'
		if(i != nb_bande-1):
			json = json + ','
		if(data == "WiFi"):
			index = index + 1
		elif((data == "ZigBee") | (data == "Bluetooth/BLE")):
			index = index + 2
	
	json = json + ']}'

	"""json = '{"nbtab":1, "tabs":[ ['+str(val_max) +','+str(val_min)+','+str(val_mean)+','+str(val_median)+','+str(val_std)+','+str(val_sum)+']]}'"""
	"""nbtab correspond au nombre de bandes de fréquences différente"""

	return json

def start_server():	
	"""Start the server."""
	server_address = ("", PORT)
	server = http.server.HTTPServer(server_address, TestHandler)
	server.serve_forever()

def charge_fichier():
	"""Lire et charger le fichier """
	fichier = open("./data.txt","r")
	fichier_entier = fichier.read()
	demi_fichier = fichier_entier.split("\n")
	tab_mots0 = demi_fichier[0].split(" ")
	tab_mots1 = demi_fichier[1].split(" ")
	colonnes = 7
	tab = [[-1] * colonnes for _ in range(nb_features)]
	index = 3
	""" index dans le fichier """
	for i in range(nb_features):
		bande = tab_mots0[index].split("-")
		tab[i][0] = bande[0]
		index = index + 6
	index = 3
	""" index dans le fichier """
	for i in range(nb_features):
		for j in range(6):
			tab[i][j+1] = tab_mots1[index]
			index = index+1
			"""pour pas commencer à 0 : correspond : 0 --> 400,500 ..."""
	fichier.close()
	return tab

start_server()
