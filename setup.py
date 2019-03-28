from setuptools import setup, find_packages

setup(name='aguaclara',
      version='0.0.24',
      description='Open source functions for AguaClara water treatment research and plant design.',
      url='https://github.com/AguaClara/aguaclara',
      author='AguaClara at Cornell',
      author_email='aguaclara@cornell.edu',
      license='MIT',
      packages=find_packages(),
      install_requires=['pint==0.8.1','numpy','pandas','matplotlib','scipy','onshapepy'],
      setup_requires=["pytest-runner"],
      tests_require=["pytest"],
      include_package_data=True,
      test_suite="tests",
      zip_safe=False)
