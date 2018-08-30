from setuptools import setup, find_packages

setup(name='aguaclara',
      version='0.0.13',
      description='AguaClara Infrastructure Design Engine',
      url='https://github.com/AguaClara/aguaclara_design',
      author='AguaClara at Cornell',
      author_email='aguaclara@cornell.edu',
      license='MIT',
      packages=find_packages(),
      install_requires=['pint','numpy','pandas','matplotlib','scipy'],
      include_package_data=True,
      test_suite="tests",
      zip_safe=False)
