from setuptools import setup, find_packages

setup(
    name='eui_fit.py',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'my_start=my_package.__main__:main',
        ]
    },
    install_requires=[
        'numpy',
        'pymoo',
        'bokeh'
    ],
)
