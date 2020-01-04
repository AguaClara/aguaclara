from setuptools import setup, find_packages

setup(
    name = 'aguaclara',
    version = '0.1.15',
    description = (
        'An open-source Python package for designing and performing research '
        'on AguaClara water treatment plants.'
    ),
    url = 'https://github.com/AguaClara/aguaclara',
    author = 'AguaClara Cornell',
    author_email = 'aguaclara@cornell.edu',
    license = 'MIT',
    packages = find_packages(),

    # Ensure that this matches Pipfile > [packages]
    install_requires = [
        'matplotlib==3.0.3', # Supports Python 3.5
        'urllib3',
        'pint==0.8.1',
        'pandas',
        'scipy',
    ],

    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    include_package_data=True,
    test_suite="tests",
    zip_safe=False
)
