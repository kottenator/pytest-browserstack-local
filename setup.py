from setuptools import setup, find_packages


setup(
    name='pytest-browserstack-local',
    version='0.5.0',
    description='``py.test`` plugin to run ``BrowserStackLocal`` in background.',
    long_description=(
        'May be useful for Continuous Integration. '
        '`Read more <https://github.com/kottenator/pytest-browserstack-local>`_.'
    ),
    url='https://github.com/kottenator/pytest-browserstack-local',
    author='Rostyslav Bryzgunov',
    author_email='kottenator@gmail.com',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'pytest>=3.0',
        'pytest-variables>=1.5.0'
    ],
    extras_require={
        'test': [
            'flake8~=3.5',
            'pytest-selenium~=1.11',
            'pytest-localserver~=0.4'
        ]
    },
    entry_points={
        'pytest11': [
            'browserstack_local = pytest_browserstack_local.plugin'
        ]
    },
    classifiers=[
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ]
)
