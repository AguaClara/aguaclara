from setuptools import setup

setup(name='aide_design',
      version='v0.0.0',
      description='AguaClara Infrastructure Design Engine',
      url='https://github.com/AguaClara/aguaclara_design',
      author='AguaClara at Cornell',
      author_email='aguaclara@cornell.edu',
      license='MIT',
      packages=['aide_design'],
      install_requires=['pint','numpy','pandas','matplotlib'],
      include_package_data=True,
      zip_safe=False)