from distutils.core import setup

setup(
    name='Django-Easy-Scoping',
    version='0.1dev',
    packages=['easy_scoping'],
    license='BSD',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=[
        'Django>=1.11,<3.0',
        'requests',
    ],
    long_description=open('README.txt').read(),
)
