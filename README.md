syscadad-api
============
API en Python para el sistema de gestión de alumnos SysAcad.

Uso
---
```python
import sysacad

s = sysacad.SysacadSession('40321', 'examplepassword')
materias = s.listMateriasPlan()
```
