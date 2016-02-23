# _*_ coding: utf-8 _*_ 
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-instapush',
    version='1.0.3',
    author='Amyth Arora',
    author_email='mail@amythsingh.com',
    packages=find_packages(),
    url='https://github.com/amyth/django-instapush',
    license='MIT License',
    description='Send push notifications to android and ios devices',
    long_description='Django Instapush can be used to send GCM and APNS '\
            'notifications to android and ios devices respectively. This '\
            'package supports both mysql and mongoengine models to store '\
            'device data',
    zip_safe=False,
    install_requires=[
        'requests>=2.8.1',
        'requests-toolbelt>=0.4.0'
    ]
)
