from setuptools import setup, find_packages

version = '1.0'

long_description = (
    open('README.md').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='ccmigration',
      version=version,
      description="Cantiericasa migration tool",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Odoo",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='',
      author='Giorgio Borelli',
      author_email='',
      url='',
      license='gpl',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'erppeek'
      ],
      extras_require={
          'test': [
              'mock',
          ]
      },
      entry_points="""
      [console_scripts]
      ccmigration = ccmigration.script:main
      """
      )
