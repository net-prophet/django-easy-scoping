import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='django-easy-scoping',
    version='1.13',
    author='Net Prophet',
    author_email='wellsroberte@gmail.com',
    packages=setuptools.find_packages(),
    url='https://github.com/net-prophet/django-easy-scoping',
    description='A mixin to allow users to create scopes on Django models.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='BSD',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=[
        'Django>=1.11,<3.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='django python scope scoping aggregate',
    project_urls={
        'Docs': 'https://net-prophet.github.io/django-easy-scoping/',
        'Usage': 'https://net-prophet.github.io/django-easy-scoping/docs/usage.html',
        'API': 'https://net-prophet.github.io/django-easy-scoping/docs/api.html',
    }
)
