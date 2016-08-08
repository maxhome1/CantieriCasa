Introduction
============

Ansible role to configure odoo service for Cantieri navali casa



Dependencies
------------

* Ansible 1.8.4
* ANXS.postgresql

::

    $ ansible-galaxy install -p roles ANXS.postgresql



Usage
-----

To install a new environment use this command::

    $ ansible-playbook -i inventories/[staging | production ] site.yml


to update an environment use this one::

    $ ansible-playbook -i inventories/[staging | production ] site.yml --tags=update

