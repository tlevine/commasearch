from distutils.core import setup

from commasearch import __version__

setup(name='commasearch',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Easily dump python objects to files, and then load them back.',
      url='https://github.com/tlevine/commasearch',
      packages=['commasearch'],
      install_requires = [],
      tests_require = ['nose'],
      version=__version__,
      license='AGPL',
)
