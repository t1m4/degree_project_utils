from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
print(requirements)
setup(
    name='myn_utils',
    version='1.0.0',
    description='utils service',
    packages=find_packages(exclude=['tests*']),
    python_requires='>=3.7',
    install_requires=requirements,
)
