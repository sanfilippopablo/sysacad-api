from distutils.core import setup

setup(
    name='sysacad-api',
    version='0.1.0',
    author='Pablo Sanfilippo',
    author_email='sanfilippopablo@gmail.com',
    packages=['sysacad_api'],
    url='http://pypi.python.org/pypi/sysacad-api/',
    license='LICENSE.txt',
    description='API para el sistema de gestión de alumnos  de UTN Sysacad.',
    long_description=open('README.rst').read(),
    install_requires=[
        "requests >= 2.0.0",
	"BeautifulSoup4 >= 4.0",
    ],
)
