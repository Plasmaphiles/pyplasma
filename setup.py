from setuptools import setup, find_packages

setup(
    name='pyplasma',
    version='0.1.0',
    description='A Python library for Plasma interaction',
    author='Zachary Westerman',
    author_email='westerman.zachary@gmail.com',
    packages=find_packages(),
    python_requires='>=3.10',
    install_requires=[
        'typing',
        'pathlib',
    ],
)
