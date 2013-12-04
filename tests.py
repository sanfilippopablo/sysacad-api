import unittest
from tests_data import *
from sysacad_api import SysacadSession

class TestLogin(unittest.TestCase):

	def setUp(self):
		pass

	def test_correct_login(self):
		sysacad = SysacadSession(BASE_URL)
		sysacad.login(LEGAJO, PASSWORD)

	def test_login_without_data(self):
		sysacad = SysacadSession(BASE_URL)
		self.assertRaises(SysacadSession.AuthenticationError, sysacad.login, '', '')

	def test_login_with_incorrect_password(self):
		sysacad = SysacadSession(BASE_URL)
		self.assertRaises(SysacadSession.AuthenticationError, sysacad.login, LEGAJO, PASSWORD + '123')

	def test_login_with_incorrect_legajo(self):
		sysacad = SysacadSession(BASE_URL)
		self.assertRaises(SysacadSession.AuthenticationError, sysacad.login, LEGAJO + '123', PASSWORD)

class TestEstadoAcademicoData(unittest.TestCase):

	def setUp(self):
		sysacad = SysacadSession(BASE_URL)
		sysacad.login(LEGAJO, PASSWORD)
		self.estado_academico_data = sysacad.estado_academico_data()


	def test_nombre_apellido(self):
		self.assertEqual(self.estado_academico_data['datos_alumno'], ('Pablo', 'Sanfilippo'))

	

def main():
	unittest.main()

if __name__ == '__main__':
	main()