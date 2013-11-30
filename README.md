syscadad-api
============
API en Python para el sistema de gestión de alumnos SysAcad.

Uso
---
```python
import sysacad

s = sysacad.SysacadSession(base_url='http://www.alumnos.frro.utn.edu.ar')
s.login('45678', 'examplepassword')
al = s.datosAlumno()
```
