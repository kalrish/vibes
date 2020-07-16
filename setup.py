import setuptools


packages = setuptools.find_namespace_packages(
    include=[
        'mustup.*',
    ],
)

setuptools.setup(
    install_requires=[
        'mustup_tup >= 0.1 , < 1.0',
        'PyYAML == 5.3.1',
    ],
    entry_points={
        'console_scripts': [
            'mustup = mustup.core.cli.main:entry_point',
        ],
    },
    name='mustup_core',
    packages=packages,
    python_requires='>= 3.8',
    version='0.1',
    zip_safe=False, # due to namespace package
)
