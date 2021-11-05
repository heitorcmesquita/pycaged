from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
classifiers = ['Operating System :: Microsoft :: Windows :: Windows 10',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3.8"]
   

#Calling setup
setup(
    name = 'pycaged',
    version = '1.6',
    description = 'fetches CAGED microdata / busca microdados do CAGED',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url = '',
    author = 'Heitor Caixeta',
    author_email = 'heitor.ca.mesquita@gmail.com',
    license = 'MIT',
    classifiers = classifiers,
    keywords = ['caged', 'ibge', 'emprego'],
    packages = find_packages(),
    include_packages_data = True,
    install_requires = ['py7zr','pandas','wget'],
    zip_safe = False)



