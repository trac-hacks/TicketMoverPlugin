from setuptools import setup

version = '0.4.2'

#this plugin was originally by Jeff Hammel <jhammel@openplans.org>
#but I've substantially altered and mainted it for a while now.

setup(name='TicketMoverPlugin',
      version=version,
      description="move tickets from one Trac to a sibling Trac",
      author='Nathan Bird',
      author_email='nathan@acceleration.net',
      url='https://github.com/UnwashedMeme/TicketMoverPlugin',
      keywords='trac plugin',
      license="BSD",
      py_modules=['ticketmoverplugin'],
      install_requires=[
          'TracSQLHelper'
      ],
      dependency_links=[
          "svn+https://trac-hacks.org/svn/tracsqlhelperscript/1.2/#egg=TracSQLHelper",
      ],
      entry_points={
          'trac.plugins': [
              'ticketmoverplugin=ticketmoverplugin'
          ]
      },
)
