 # -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
from conf import *

class SysacadSession:
	"Sesión de SysCAD."

	url = URLS_DICT

	def __init__(self, legajo=None, password=None, base_url=DEFAULT_BASE_URL):
		self.base_url = base_url
		self.login_data = {
			'legajo': legajo,
			'password': password,
		}

	def _get(self, url_action):
		self.login()
		url = self.base_url + url_action
		return requests.get(url, cookies=self.cookies) 

	def _post(self, url_action, data):
		self.login()
		url = self.base_url + url_action
		return requests.post(url, cookies=self.cookies, data=data)

	def login(self):

		# Make request
		url = self.base_url + self.url['login']
		response = requests.post(url, data=self.login_data)

		# Handle incorrect login
		html = BeautifulSoup(response.text)
		if html.title.string == u'Ingreso Alumnos al SYSACAD' or html('p', attrs={'class': "textoError"}):
			raise Exception('Información de login incorrecta.')

		# Store session cookie
		for key in response.cookies.keys():
			if key.find(SESSION_COOKIE_NAME):
				break
		self.cookies = {key: response.cookies[key]}

	def _getInfoFromTable(self, url):
		response = self._get(url)
		html = BeautifulSoup(response.text)
		trs = []
		for tr in html('tr', attrs={'class': "textoTabla"}):
			tds = []
			for td in tr('td'):
				tds.append(td.string)
			trs.append(tds)
		del trs[0]
		return trs

	def listMateriasPlan(self):
		materias = self._getInfoFromTable(self.url['materias_plan'])
		data = []
		for materia in materias:
			data.append({
				'anio': materia[0],
				'duracion': materia[1],
				'nombre': materia[2],
				'se_cursa': materia[3],
				'se_rinde': materia[4]
			})
		return data


	def estadoAcademico(self):
		materias = self._getInfoFromTable(self.url['estado_academico'])
		data = []
		for materia in materias:
			data.append({
				'anio': materia[0],
				'nombre': materia[1],
				'estado': materia[2],
				'plan': materia[3]
			})
		return data

def main():
	s = SysacadSession('40261', 'am3toktf99')
	print s.estadoAcademico()

if __name__ == '__main__':
	main()