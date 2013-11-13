 # -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup

class SysACADSession:
	"Sesión de SysCAD."
	base_url = 'http://www.alumnos.frro.utn.edu.ar/'
	url = {
		'login': 'menuAlumno.asp',
	}

	def __init__(self, legajo=None, password=None):
		self.legajo = legajo
		self.password = password
		self.login()	
	
	def login(self):
		url = self.base_url + self.url['login']
		login_data = {'legajo': self.legajo, 'password': self.password}
		response = requests.post(url, data=login_data)
		html = BeautifulSoup(response.text)
		print html.title.string

def main():
	s = SysACADSession('40261', '28357987')

if __name__ == '__main__':
	main()