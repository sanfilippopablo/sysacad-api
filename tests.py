import unittest
from tests_data import *
import sysacad_api

class TestEstadoAcademicoData(unittest.TestCase):

	def setUp(self):
		sysacad = sysacad_api.SysacadSession(BASE_URL)
		sysacad.login(LEGAJO, PASSWORD)
		self.estado_academico_data = sysacad.estado_academico_data()


	def test_nombre_apellido(self):
		self.assertEqual(self.estado_academico_data['datos_alumno'], ('Pablo', 'Sanfilippo'))

	

def main():
	unittest.main()

if __name__ == '__main__':
	main()