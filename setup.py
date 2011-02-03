#!/usr/bin/env python
from distutils.core import setup
import os
from ckeditor_widget import VERSION
path='ckeditor_widget'

long_description = open('README.txt').read()
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk(path):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[(len(path)+1):] # Strip "admin_tools/" or "admin_tools\"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))

setup(
    name='django-ckeditor-widget',
    version='0.0',
    description='custom widget for django-ckeditor',
    long_description=long_description,
    author='NORD',
    author_email='nordmenss@gmail.com',
    url='https://github.com/nordmenss/django-ckeditor-widget',
    package_dir={path: path},
    packages=packages,
    package_data={path: data_files},
    classifiers=[
        'Development Status :: 0 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    install_requires=['django-ckeditor'],
    zip_safe=False,
)
