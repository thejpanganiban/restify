from setuptools import setup, find_packages


setup(name="Restify",
      description="A RESTful interface for Mongodb",
      version='0.1',
      packages=find_packages(),
      entry_points={
          'console_scripts': ['restify.debug = restify.server:debug']
        },
      install_requires=[
          'flask >= 0.8, < 0.9',
          'pymongo >= 2.2, < 2.3',
        ],
      )
