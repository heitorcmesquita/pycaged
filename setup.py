from setuptools import setup, find_packages

classifiers = ['Operating System :: Microsoft :: Windows :: Windows 10',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3.8"]
   

#Calling setup
setup(
    name = 'pycaged',
    version = '0.2',
    description = '',
    long_description = open('README.txt').read(),
    url = '',
    author = 'Heitor Caixeta',
    author_email = 'heitor.ca.mesquita@gmail.com',
    license = 'MIT',
    classifiers = classifiers,
    keywords = 'caged',
    packages = find_packages(),
    include_packages_data = True,
    install_requires = ['py7zr','pandas','wget'],
    entry_points = {
        'console_scripts':[
            'testecaged=testecaged.__main__:main',
            ]
        },
    zip_safe = False)



