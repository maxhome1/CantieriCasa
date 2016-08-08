Extra packages
==============

Somethime we need to include some package repository in OpenERP project.

To include a package repository in OpenERP you should edit `conf/packages.cfg`file and include the repository in this way::


    [openerp]
    addons +=
        ...
        bzr lp:account-financial-tools/7.0 ${buildout:directory}/parts/account-financial-tools last:1
        ...



Here you can find some useful repository.

Accounting Analytics
--------------------

This repository aim to deal with modules related to manage analytic accounting. You'll find modules that:

* Add a multi-currency capability to analytic lines
* Handle a second analytic axis
* Improve default values
* Handle analytic distributions for more objects

::

    bzr lp:account-analytic/7.0 ${buildout:directory}/parts/account-analytic last:1


Account Budgeting
-----------------

This repository aim to deal with modules related to manage budgeting. You'll find modules that handle budget

::

    bzr lp:account-budgeting/7.0 ${buildout:directory}/parts/account-budgeting last:1


Account Closing
---------------

This repository aim to deal with modules related to manage account closing.

::

    bzr lp:account-closing/7.0 ${buildout:directory}/parts/account-closing last:1


Account Consolidation
---------------------

This project aim to deal with modules related to manage account consolidation in a generic way.

::

    bzr lp:account-consolidation/7.0 ${buildout:directory}/parts/account-consolidation last:1


Account Financial Tools
-----------------------

This repository aim to deal with modules to ease the financial accounting in OpenERP. You'll find modules that:

* Update the currency rate automatically via web services
* Credit Management and follow up
* Account reversal to generate the "contrary" of an entries with a link between them

::

    bzr lp:account-financial-tools/7.0 ${buildout:directory}/parts/account-financial-tools last:1


Account Finacial Reports
------------------------

This repository aim to deal with modules related to financial reports. You'll find modules that print legal and official reports.

::

    bzr  lp:account-financial-report/7.0 ${buildout:directory}/parts/account-financial-report last:1


Account Invoicing
-----------------

In this repository you'll find a module that permiti to force the invoice number and permit to delete a canceled invoice

::

    git git://github.com/OCA/account-invoicing.git ${buildout:directory}/parts/account-invoicing 8.0


Account Payment
---------------

This repository aim to deal with modules related to payment, bank statement and voucher functionality.

::

    bzr  lp:account-payment/7.0 ${buildout:directory}/parts/account-payment last:1


Contract management
-------------------

This repository aim to deal with modules related to manage contract in a generic way. You'll find modules that:

* Manage sold hours in advance
* Invoice on contract basis

::

    bzr lp:contract-management/7.0 ${buildout:directory}/parts/contract-management last:1


HR - TimeSheet
--------------

This repository aim to deal with modules related to manage timesheet in a generic way. You'll find modules that:

* Print extra timesheet reports
* Wizard helper to manage Timesheet Completion

::

    bzr lp:hr-timesheet/7.0 ${buildout:directory}/parts/hr-timesheet last:1


HR
--

This repository aim to deal with modules related to manage Human Resource in a generic way. You'll find modules that:

* HR Policies for contracts, working hours
* Holidays management
* Extra information on HR Contract
* Extra information on Skills, Education

::

    bzr lp:openerp-hr/7.0 ${buildout:directory}/parts/openerp-hr last:1


Italy
-----

This repository aim to deal with modules related to Italian Localization. You'll find modules that:

* DDT managements
* Var Registries
* Ri.BA. Management
* Partial deducible Vat

::

    bzr lp:openobject-italia/7.0 ${buildout:directory}/parts/openobject-italia last:1


Knowledge
---------

This repository is meant to gather all community extensions of OpenERP's knowledge and document management. Here you should find all community modules that

* Implement means to structure knowledge
* Provide access to knowledge/documents

::

    bzr lp:knowledge-addons/7.0 ${buildout:directory}/parts/knowledge-addons last:1


Management system
-----------------

This repository aim to deal with modules related to manage management systems:

* Quality (ISO 9001)
* Environment (ISO 14001)
* Security (ISO 27001, PCI-DSS)
* IT services (ISO 20001, ITIL)
* Health & Safety (OHSAS 18001)

::

    bzr lp:openerp-mgmtsystem/7.0 ${buildout:directory}/parts/openerp-mgmtsystem last:1


OpenERP connector
-----------------

This repository links to the E-Commerce Connector, a powerful framework to develop any kind of bi-directional connector between OpenERP and any other software or service.

::

    bzr  lp:openerp-connector/7.0 ${buildout:directory}/parts/openerp-connector last:1


Openerp Magento connector
-------------------------

This repository links to the Magento E-commerce management connector

::

    bzr  lp:openerp-connector-magento/7.0 ${buildout:directory}/parts/openerp-connector-magento last:1



OpenERP reporting engines
-------------------------

This repository hosts alternative reporting engines to the ones included on OpenERP core (RML and Webkit).

* XLS report engine
* Report Assembler (merge more pdf from different reports in one unique Pdf)

::

    bzr lp:openerp-reporting-engines/7.0 ${buildout:directory}/parts/openerp-reporting-engines last:1


Partner contact management
--------------------------

This project aim to deal with modules related to manage contact and partner in OpenERP. You'll find modules that:

* Improve the organization of contact
* Interface the contact with LDAP
* Split up name and first name

::

    bzr lp:partner-contact-management ${buildout:directory}/parts/partner-contact-management last:1


Server Enviroment and tools
---------------------------

This project aim to deal with modules related to manage OpenERP server environment and provide useful tools. You'll find modules that:

* Manage configuration depending on environment (devs, test, prod,..)
* Keep the security on update
* Manage email settings

::

    bzr lp:server-env-tools/7.0 ${buildout:directory}/parts/server-env-tools last:1


Web Addons
----------

This project aims to deal with modules related to the webclient of Odoo. You'll find modules that:

* Add facilities to the UI
* Add widgets
* Ease the import/export features
* Generally add clientside functionality

::

    bzr lp:web-addons/7.0 ${buildout:directory}/parts/web-addons last:1
