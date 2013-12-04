 # -*- coding: utf-8 -*-
import requests, re
from BeautifulSoup import BeautifulSoup
from conf import *


class SysacadSession(object):
	"Sesión de SysCAD."

	# Exceptions

	class AuthenticationError(Exception):
		pass

	class OperationError(Exception):
		pass

	url = URLS_DICT

	def __init__(self, base_url=None, session=None):
		self.base_url = base_url or DEFAULT_BASE_URL
		if session:
			assert isinstance(requests.Session, session), 'Object session must be instance of requests.Session.'
			self.session = session
		else:
			self.session = requests.Session()

	def _is_login_page(self, text):
		html = BeautifulSoup(text)
		if html.title.string == u'Ingreso Alumnos al SYSACAD' or html('p', attrs={'class': "textoError"}):
			return True
		return False

	def _get(self, url_action, data=None):
		url = self.base_url + url_action
		response = self.session.get(url, params=data) 

		if self._is_login_page(response.text):
			raise self.AuthenticationError('You must call .login(legajo, password).')

		return response

	def _post(self, url_action, data=None):
		url = self.base_url + url_action
		response = self.session.post(url, data=data)

		if self._is_login_page(response.text):
			raise self.AuthenticationError('You must call .login(legajo, password).')

		return response

	def login(self, legajo, password):

		url = self.base_url + self.url['login']
		response = self.session.post(url, data={'legajo': legajo,'password': password})
	
		if self._is_login_page(response.text):
			raise self.AuthenticationError('Información de login incorrecta.')

	def _data_from_table(self, bs_html, keys):
		data = []
		for tr in bs_html('tr', attrs={'class': "textoTabla"}):
			tds = {}
			i = 0
			for td in tr('td'):
				tds[keys[i]] = td.getText()
				i += 1
			data.append(tds)
		del data[0] # First row is always the table header.
		return data

	def datosAlumno(self):
		response = self._get(self.url['estado_academico'])
		html = BeautifulSoup(response.text)
		cadena = html('td', attrs={'class': "tituloTabla"})[0].getText()
		p = re.compile(ur'Estado académico de (.*), (.*) al .* PM')
		data = p.search(cadena).groups()
		return {'nombre': data[1], 'apellido': data[0]}

	def materiasEnCurso(self):
		estado_academico = self.estadoAcademico()
		materias = []
		for materia in estado_academico:
			if materia['estado'].find('Cursa') != -1:
				materias.append(materia['nombre'])
		return materias

	def estado_academico_data(self):
		# Inicializar
		data = {}
		response = self._get(self.url['estado_academico'])
		html = BeautifulSoup(response.text)

		# Datos alumno
		cadena = html('td', attrs={'class': "tituloTabla"})[0].getText()
		p = re.compile(ur'Estado académico de (.*), (.*) al .*')
		groups = p.search(cadena).groups()
		data['datos_alumno'] = groups[1], groups[0]

		#Datos de la materia
		data['materias'] = []
		keys = ('anio', 'nombre', 'estado', 'plan')
		materias = self._data_from_table(html, keys)

		aprobadas_regex = re.compile(ur'Aprobada con (\d*) Tomo: (\d*) Folio: (\d*)')
		cursa_regex = re.compile(ur'Cursa en (.*) Aula (.*)')
		regular_regex = re.compile(ur'Regularizada en (\d*)( \(.*\))?')

		for mat in materias:
			materia = {}
			materia['anio'] = mat['anio']
			materia['nombre'] = mat['nombre']
			materia['plan'] = mat['plan']

			match = aprobadas_regex.search(mat['estado'])
			if match != None:
				groups = match.groups()
				materia['estado'] = {
					'estado': 'aprobada',
					'nota': groups[0],
					'tomo': groups[1],
					'folio': groups[2],
				}
				data['materias'].append(materia)
				continue

			match = cursa_regex.search(mat['estado'])
			if match != None:
				groups = match.groups()
				materia['estado'] = {
					'estado': 'cursa',
					'comision': groups[0],
					'aula': groups[1],
				}
				data['materias'].append(materia)
				continue

			match = regular_regex.search(mat['estado'])
			if match != None:
				groups = match.groups()
				materia['estado'] = {
					'estado': 'regular',
					'anio': groups[0],
				}
				data['materias'].append(materia)
				continue

			materia['estado'] = {'estado': 'no_inscripto'}
			data['materias'].append(materia)

		return data

	def change_password(self, old_pass, new_pass):
		data = {
			'passwordActual': old_pass,
			'password': new_pass,
			'pruebaPassword': new_pass,
		}
		response = self._post(self.url['change_password'], data=data)
		if not response.text.find('cambiada correctamente'):
			raise self.OperationError('Contraseña no cambiada correctamente.')