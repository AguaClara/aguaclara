from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

setup_requirements = []

test_requirements = [
    "black",
    "flake8",
    "codecov",
    "pytest",
    "pytest-cov",
    "pytest-html",
]

dev_requirements = [
    *setup_requirements,
    *test_requirements,
    "Sphinx",
    "sphinx-rtd-theme",
    "tox",
    "matplotlib",
    "ipykernel"
]

requirements = [
    "matplotlib",
    "urllib3",
    "pint",
    "pandas",
    "scipy",
    "onshape_client",
    "numpy",
]

extra_requirements = {
    "setup": setup_requirements,
    "test": test_requirements,
    "dev": dev_requirements,
    "all": [
        *requirements,
        *dev_requirements,
    ],
}

setup(
    name = "aguaclara",
    version = "0.4.0",
    description = (
        "An open-source Python package for designing and performing research "
        "on AguaClara water treatment plants."
    ),
    long_description = readme,
    long_description_content_type="text/markdown",
    url = "https://github.com/AguaClara-Reach/aguaclara",
    project_urls = {
        "Documentation": "https://aguaclara-reach.github.io/aguaclara/"
    },
    author = "AguaClara Reach",
    author_email = "mwebershirk@aguaclarareach.org",
    license = "MIT",
    classifiers = [
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages = find_packages(),
    # Ensure that this matches Pipfile > [packages]
    install_requires=requirements,
    # Ensure that this matches Pipfile > [dev-packages]
    test_requires=test_requirements,
    extras_require=extra_requirements,
    python_requires=">=3.8",
    setup_requires=["pytest-runner"],
    tests_require=["pytest==7.2.1", "codecov>=2.1.4"],
    include_package_data=True,
    test_suite="tests",
    zip_safe=False
)
