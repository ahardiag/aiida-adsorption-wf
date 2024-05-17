from setuptools import setup,find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='EQeq_raspa_aiida',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=required,
    author='Arthur Hardiagon',
    author_email='arthur.hardiagon@chimieparistech.psl.eu',
)