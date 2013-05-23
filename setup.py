from setuptools import find_packages, setup

version='0.2.2'

setup(name='TicketMoverPlugin',
      version=version,
      description="move tickets from one Trac to a sibling Trac",
      author='Jeff Hammel',
      author_email='jhammel@openplans.org',
      url='http://trac-hacks.org/wiki/k0s',
      keywords='trac plugin',
      license="",
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests*']),
      include_package_data=True,
      package_data={'ticketmoverplugin': ['templates/*', 'htdocs/*']},
      zip_safe=False,
      install_requires=[
          'TracSQLHelper'
      ],
      dependency_links=[
          "http://trac-hacks.org/svn/tracsqlhelperscript/anyrelease#egg=TracSQLHelper",
      ],
      entry_points="""
      [trac.plugins]
      ticketmoverplugin = ticketmoverplugin.ticketmover
      """,
      )
