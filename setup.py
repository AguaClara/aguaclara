from setuptools import setup

setup(name='AIDE',
      version='0.0',
      description='AguaClara Infrastructure Design Engine',
      url='https://github.com/AguaClara/aguaclara_design',
      author='AguaClara at Cornell',
      author_email='aguaclara@cornell.edu',
      license='MIT',
      packages=['AIDE'],
      install_requires=['pint','numpy','pandas','matplotlib'],
      zip_safe=False)