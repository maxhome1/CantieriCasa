How to develop a policy package
===============================

1. Download `abstract_bootstrap <http://git.abstract.it/abstract-collective/abstract-bootstrap>`_
2. Go to `src`directory of this buildout
3. Run this command::

    $ python abstract_bootstrap.py openerp_policy <name> [target_repository]

4. include the package <name> in `conf/packages.cfg`in this form::

    [sources]
    <name> = git <repository_url> egg=False

5. run buildout e start OpenERP
