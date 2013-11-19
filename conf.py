 # -*- coding: utf-8 -*-

SESSION_COOKIE_NAME = 'ASPSESSIONID'

URLS_DICT = {
		'login': 'menuAlumno.asp',
		'materias_plan': 'materiasPlan.asp',
		'estado_academico': 'estadoAcademico.asp',
		'correlatividad_cursado': 'correlatividadCursado.asp',
	}


# URL en la que se encuentra montado Sysacad según facultad regional.
DEFAULT_BASE_URL = 'http://www.alumnos.frro.utn.edu.ar/'