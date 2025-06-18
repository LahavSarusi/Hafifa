from setuptools import setup, find_packages

setup(
    name='your_package_name',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'Flask-SQLAlchemy',
        'pydantic==2.7.1',
        'Flask==2.2.5',
        'Flask-RESTful',
        'pytest',
        'flasgger',
        'pydantic==2.7.1',
        'pyodbc',
        'Flask-SocketIO'
    ],
    tests_require=[
        'pytest'
    ]
)
