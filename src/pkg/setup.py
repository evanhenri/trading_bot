import io
import os

from setuptools import find_packages, setup


ROOT = os.path.abspath(os.path.dirname(__file__))


NAME = 'trader'
DESCRIPTION = 'Cryptocurrency trading bot.'
URL = ''
EMAIL = 'e.henri90@gmail.com'
AUTHOR = 'Evan Henri'


REQUIRED = [
    'asyncpgsa',
    'autobahn',
    'celery',
    'redis',
    'hiredis',
    'matplotlib',
    'psycopg2',
    'scipy',
    'sqlalchemy',
    'sklearn',
    'tensorflow',
    'twisted',
    'ipython'
]


with io.open(os.path.join(ROOT, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


about = {}
with open(os.path.join(ROOT, NAME, '__version__.py')) as f:
    exec(f.read(), about)


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(
        exclude=(
            'tests',
        )
    ),
    py_modules=[
        'trader'
    ],
    install_requires=REQUIRED,
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
