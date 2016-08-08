OpenERP Buildout
================

A base buildout for your OpenERP project.

Structure
---------

The `conf` folder contains the basic buildout for openerp.

This file contains al general configuration for all environments.
You can override and extend different configurations:

* base.cfg

These files define specific configuration per environment:

* development.cfg
* staging.cfg
* production.cfg
* demo.cfg


There are these files that can be included in base.cfg o any other files
accordingly to the project needs:

* openerp.cfg - included in base.cfg
* ldap.cfg
* postgresql.cfg
* wkhtmltopdf.cfg
* supervisor.cfg


Get started
-----------

Copy the example buildout::

	cp buildout.cfg.example buildout.cfg

and select a specific file to extend according to environment you want to install:

* conf/production.cfg
* conf/staging.cfg
* conf/development.cfg

Packages and extensions related to a specific project
should be included in this file:

* conf/packages.cfg

Note: many configuration can be overridden by change variables in ``[config]`` part.

Additional Dependencies
-----------------------
  libxml2-dev
  libxslt-dev
  libldap2-dev
  libsasl2-dev
  python-cups
  libcups2-dev


Add custom packages
-------------------

When adding your packages to this buildout you must use this syntax::

    [openerp]
    addons +=
        git git@git.abstract.it:openerp-abstract/hr-rent.git ${buildout:directory}/parts/hr_rent master

Unlike mr.developer, this will create a nested dir like::

    src/hr_rent/hr_rent


LDAP configuration
==================

You can add ``conf/ldap.cfg`` to your buildout in order to compile python-ldap package.

make sure you have installed these dependencies on your system before to run the buildout (these packages are available in a Debian like environment):

* libssl-dev
* libredline5-dev
* libldap2-dev
* libsasl2-dev


Deploy
======

Dependencies:

* Ansible 1.8.4
* ANXS.postgresql

See: deploy/README.txt


Sphinx Documentation
====================

This buildout contains Sphinx documentation that can be built in this way::

1. Add ``docs/sphinx.cfg``file in your buildout.cfg
2. Run the buildout
3. compile spinx sources by this command  ``./bin/sphinx``

You can read the documentation by pointing your Web browser to this location::

    file:///{buildout_directory}/docs/html/index.html

