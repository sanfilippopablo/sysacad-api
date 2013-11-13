 # -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
from conf import *

class SysACADSession:
	"Sesión de SysCAD."

	url = URLS_DICT

	def __init__(self, legajo=None, password=None, base_url=DEFAULT_BASE_URL):
		self.base_url = base_url
		self.login_data = {
			'legajo': legajo,
			'password': password,
		}

	def login(self):

		# Make request
		url = self.base_url + self.url['login']
		response = requests.post(url, data=self.login_data)

		# Handle incorrect login
		html = BeautifulSoup(response.text)
		if html.title.string == u'Ingreso Alumnos al SYSACAD' or html('p', attrs={'class': "textoError"}):
			raise Exception('Información de login incorrecta.')

		# Store session cookie
		self.cookies = {SESSION_COOKIE_NAME: response.cookies[SESSION_COOKIE_NAME]}