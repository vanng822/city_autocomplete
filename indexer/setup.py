from setuptools import setup

setup(
    name='City Autocomplete Indexer',
    version='0.1',
    long_description=__doc__,
    packages=['city_indexer'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['elasticsearch']
)