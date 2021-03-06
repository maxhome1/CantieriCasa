Introduction
============

This package provides a command line script to perform Odoo migrations.
It also contains some classes for many model migrations.

For more documentation, please refer to:
https://docs.google.com/document/d/1yrF1xg15zGSHDKQqBSNQ8xjmv6ZLZDstsPxxUzccY6w/


Installation
============

Dependencies
------------

* erppeek


Include erppeek and ccmigration eggs in your buildout configuration and generates all the necessary scripts::


    parts =
        ...
        openerp
        migration
        erppeekini

    [openerp]
    recipe = anybox.recipe.openerp
    eggs =
        ...
        erppeek

    [source]
    ccmigration = git git@git.abstract.it/cantiericasa/ccmigration.git

    [migration]
    # installs erppeek and arpesmigration scripts in bin folder
    recipe = zc.recipe.egg:scripts
    eggs =
        erppeek
        ccmigration

    [erppeekini]
    recipe = collective.recipe.template
    input = ${buildout:directory}/templates/erppeek.in
    output = ${buildout:directory}/etc/erppeek.ini


Usage
=====

Create `erppeek.ini` file that contains source and destination configurations, for example::

    [source]
    username = admin
    password = admin
    host = localhost
    port = 9569
    database = openerp6

    [destination]
    username = admin
    password = admin
    host = localhost
    port = 8069
    database = odoo8


Launch the script in this way::

    $ bin/migration <migration name> -s <source env>  -d <destination env> -c <path/to/erppeek.ini> -l <limit number of record> -o <offset to start from>


Cantiericasa Details
--------------------

* Once Odoo is installed, edit admin permissions by checking the **Funzionalità tecniche** flag.

* Update the list of modules.

* Install the ``cc_base`` module, a container for all *cantieri casa* dependencies.

* Choose *Cantieri Casa Account Charts* as **Template del piano dei conti**.

* Go to **Vendite > Configurazione > Rubrica > Importa da GeoNames** and import the Italia package.

* Go to **Vendite > Configurazione > Rubrica > Stati Federali** and change *Reggio Dell'Emilia* to *Reggio Emilia* and *Bolzano/Bozen* in *Bolzano*.

* Go to **Configurazione > Vendite** and check *Allow using different units of measure* or similar.

* Go to **Configurazione > Contabilità** and choose *Arrotondamento sul Totale* from the *Metodo di arrotondamento delle imposte* dropdown.

* Go to **Configurazione > Magazzino** and check *Track lots or serial numbers*.

* Go to **Configurazione > Produzione** and check *Gestisce routings e ordini di lavoro*.

* Go to **Magazzino > Configurazione > Dati DdT > Causali trasporto** and create a new transportation reason called *Conto Lavorazione*.

* Create new ``x_uuid`` fields for ``account.move``, ``account.move.line``, ``account.voucher``, ``account.voucher.line``,  ``account.invoice``, ``account.move.reconcile`` and ``product.product`` models using the web interface, both on the old system and on the new one.

* Run these script in this order:

        $ ./bin/ccmigration populate_uuid -c etc/erppeek.ini
        $ ./bin/ccmigration dummydata -c etc/erppeek.ini
        $ ./bin/ccmigration users -c etc/erppeek.ini
        $ ./bin/ccmigration accountpaymentterm -c etc/erppeek.ini
        $ ./bin/ccmigration accountperiod -c etc/erppeek.ini
        $ ./bin/ccmigration uom -c etc/erppeek.ini
        $ ./bin/ccmigration productpricelist -c etc/erppeek.ini
        $ ./bin/ccmigration bank -c etc/erppeek.ini
        $ ./bin/ccmigration partner_category -c etc/erppeek.ini
        $ ./bin/ccmigration partner -c etc/erppeek.ini
        $ ./bin/ccmigration partneraddress -c etc/erppeek.ini

* Before proceeding with the migrations below, delete one of the two *CANTIERI NAVALI CASA S.R.L.* partner, the one with the (wrong) email address info@abstract.it. Then move on:

        $ ./bin/ccmigration productcategory -c etc/erppeek.ini
        $ ./bin/ccmigration product -c etc/erppeek.ini
        $ ./bin/ccmigration productpricelistitem -c etc/erppeek.ini
        $ ./bin/ccmigration productsupplierinfo -c etc/erppeek.ini
        $ ./bin/ccmigration resource -c etc/erppeek.ini
        $ ./bin/ccmigration employee -c etc/erppeek.ini
        $ ./bin/ccmigration workcenter -c etc/erppeek.ini
        $ ./bin/ccmigration routing -c etc/erppeek.ini
        $ ./bin/ccmigration bom -c etc/erppeek.ini
        $ ./bin/ccmigration saleorder -c etc/erppeek.ini
        $ ./bin/ccmigration purchaseorder -c etc/erppeek.ini
        $ ./bin/ccmigration accountjournal -c etc/erppeek.ini
        $ ./bin/ccmigration accountanalyticaccount -c etc/erppeek.ini
        $ ./bin/ccmigration accountbankstatement -c etc/erppeek.ini
        $ ./bin/ccmigration accountmovereconcile -c etc/erppeek.ini

* Open all the account periods or it's impossible to migrate the account moves. From erppeek run ``ap = model('account.period').browse(['state=done']).read('id');model('account.period').browse([]).write({'state': 'draft'})``, then you can close again the id in the ``ap`` list.

        $ ./bin/ccmigration accountmove -c etc/erppeek.ini
        $ ./bin/ccmigration accountinvoice -c etc/erppeek.ini --debug
        $ ./bin/ccmigration accountvoucher -c etc/erppeek.ini
        $ ./bin/ccmigration stockproductionlot -c etc/erppeek.ini
        $ ./bin/ccmigration stockpicking -c etc/erppeek.ini


* The last one will fix an issue with wrong partners data:

        $ ./bin/ccmigration fix_contacts -c etc/erppeek.ini

* It might be necessary to migrate by hand those objects:
  * Product Pricelist: *Casa 48'HT 2012 rev.01*
  * Product Pricelist: *Rimessaggio Imbarcazioni 2013-2014*

**Note:** the ``--debug`` option is needed because the old database contains
 a few unreferenced objects that don't raise any error.

Manually restore the database on stage
======================================

* First create a dump of the local database and give it a name with the current day:

        pg_dump -Ft DBNAME | gzip > cantiericasaDATE.tar.gz

* Copy the database onto the stage server:

        scp cantiericasaDATE.tar.gz webapp@188.166.3.206:/srv/webapp/

* Create the database on the stage server:

        psql -U odoo
        CREATE DATABASE cantiericasaDATE;

* Finally, restore the dump:

        gunzip cantiericasaDATE.tar.gz
        pg_restore -U odoo -O -x -d cantiericasaDATE cantiericasaDATE.tar

Manual settings - after migration
----------------------------------

[TODO]

Create new migration command
============================

1. Create a new class that inherit from base.BaseCommand
2. Import it in script file and add a new item in command dictionary::

        commands = {
            ...
            'mycommand': MyCommandClass
        }

3. Override *get_migration_data* method by defining these attributes:
    * self.source_model: Odoo 6 - res.partner
    * self.dest_model: Odoo 8 - res.partner
    * self.source_model_ids: all partner ids
    * self.source_data: all partner objects

4. Customize *check_existent* method to search for duplicated records.

5. Define *_fields* property to manage source and destination fields mapping.


_fields attribute specifications
--------------------------------

**_fields** is a dictionary and each item reptresents a specific model's field.

Each dictionary key defines a source models field and the value specifies
the tranformations needed for the migration to destination model.

Example:

1. fields with the same name and same value type::

        _fiels = {
            <source_fieldname>: None
            ...
        }

2. fields with the same value but different names::

        _fiels = {
            <source_fieldname>: {"name": <destination_fieldname>}
            ...
        }

3. Simple Many2One relation::

        _fields = {
            <source_fieldname>: {
                'name': <destination_fieldname>,
                'type': 'm2o',
                'unique_field': <fieldname>,  # Optional attribute used
                                              # to search for and create
                                              # related record
                                              # default: 'name'
                'relation': <related.model.in.dotted.name>  # eg: res.partner.title,
                'create': True|False  # create resource if not found or not
            }
            ...
        }

4. Simple Many2Many relation::

        _fields = {
            <source_fieldname>: {
                'name': <destination_fieldname>,
                'type': 'm2m',
                'relation': <related.model.in.dotted.name>  # eg: res.partner.title,
                'create': True|False  # create resource if not found or not
            }
            ...
        }

5. Custom fields, a field can be defined by a custom function
   that takes two parameters: Old ERP record, new value (as dictionary). Eg.::

        _fields = {
            <source_fieldname>: {
                'type': 'custom',
                'setter': <custom_function>
            }
            ...
        }

Default values
--------------

For any migrations it can be defined some default values in this way::

        _default_values = {
            "<field_name>": <value>
        }

these value will be used for all record created.




[3708/3717] Create product.product - Girante per pompa Jabsco - 3709
[3709/3717] Create product.product - Copriparabordo F6 - 3710
[3710/3717] Create product.product - Copriparabordo A5 - 3711
[3711/3717] Create product.product - Sensore di livello Nafta 4-20mA Danfoss - 3712
[3712/3717] Create product.product - Antivegetativa Veneziani DRP100 Rosso , conf. da 10 L - 3713
[3713/3717] Create product.product - Tagliando motori Volvo Penta 225CV - 3714


[242/274] Create product.pricelist.item - 30% - 172
[243/274] Create product.pricelist.item - 43710 - 173
[244/274] Create product.pricelist.item - 43712 - 174
[245/274] Skip product.pricelist.item - 43710
[246/274] Skip product.pricelist.item - 43712
[247/274] Create product.pricelist.item - 76020/54 - 175
[248/274] Create product.pricelist.item - Sconto 30% - 176
Traceback (most recent call last):
  File "/srv/webapp/staging/odoo/src/ccmigration/src/ccmigration/base.py", line 507, in main
    migrator.migrate()
  File "/srv/webapp/staging/odoo/src/ccmigration/src/ccmigration/base.py", line 412, in migrate
    record = self.build_record(data)
  File "/srv/webapp/staging/odoo/src/ccmigration/src/ccmigration/base.py", line 288, in build_record
    transform=f_transform
  File "/srv/webapp/staging/odoo/src/ccmigration/src/ccmigration/base.py", line 199, in _get_relation_id_by_field
    raise KeyError(msg)
KeyError: u'Value not found for product.pricelist.version - Rimessaggio Imbarcazioni 2013-20



OPEN PERIODS ID [14,
 15,
 16,
 17,
 18,
 19,
 20,
 21,
 22,
 23,
 24,
 25,
 50,
 51,
 26,
 27,
 28,
 29,
 30,
 31,
 32,
 33,
 34,
 35,
 36,
 37,
 52]



 model('account.account').browse(['name=C/MERCI VENDITE']).write({'code':'2002/01/01'})


 [3447/3495] Create account.move - 3126 - 4281
 [3448/3495] Create account.move - 3127 - 4282
 Traceback (most recent call last):
   File "/srv/webapp/staging/odoo/src/ccmigration/src/ccmigration/base.py", line 506, in main
     migrator.migrate()
   File "/srv/webapp/staging/odoo/src/ccmigration/src/ccmigration/accountmove.py", line 350, in migrate
     super(AccountMoveMigration, self).migrate()
   File "/srv/webapp/staging/odoo/src/ccmigration/src/ccmigration/base.py", line 412, in migrate
     record = self.build_record(data)
   File "/srv/webapp/staging/odoo/src/ccmigration/src/ccmigration/base.py", line 315, in build_record
     setter(el, record)
   File "/srv/webapp/staging/odoo/src/ccmigration/src/ccmigration/accountmove.py", line 316, in _set_move_line
     raise KeyError("Tax code '%s' not found even in the mapping" % line.tax_code_id.name)
 KeyError: "Tax code '13,73% (credito)' not found even in the mapping"

 [4/47] Create account.move - EXJ/2015/1140 - 4286
 Traceback (most recent call last):
   File "/srv/webapp/staging/odoo/src/ccmigration/src/ccmigration/base.py", line 506, in main
     migrator.migrate()
   File "/srv/webapp/staging/odoo/src/ccmigration/src/ccmigration/accountmove.py", line 350, in migrate
     super(AccountMoveMigration, self).migrate()
   File "/srv/webapp/staging/odoo/src/ccmigration/src/ccmigration/base.py", line 412, in migrate
     record = self.build_record(data)
   File "/srv/webapp/staging/odoo/src/ccmigration/src/ccmigration/base.py", line 315, in build_record
     setter(el, record)
   File "/srv/webapp/staging/odoo/src/ccmigration/src/ccmigration/accountmove.py", line 316, in _set_move_line
     raise KeyError("Tax code '%s' not found even in the mapping" % line.tax_code_id.name)
 KeyError: "Tax code 'Ritenute da Versare' not found even in the mapping"

Traceback (most recent call last):
  File "/srv/webapp/staging/odoo/src/ccmigration/src/ccmigration/base.py", line 506, in main
    migrator.migrate()
  File "/srv/webapp/staging/odoo/src/ccmigration/src/ccmigration/accountmove.py", line 350, in migrate
    super(AccountMoveMigration, self).migrate()
  File "/srv/webapp/staging/odoo/src/ccmigration/src/ccmigration/base.py", line 412, in migrate
    record = self.build_record(data)
  File "/srv/webapp/staging/odoo/src/ccmigration/src/ccmigration/base.py", line 315, in build_record
    setter(el, record)
  File "/srv/webapp/staging/odoo/src/ccmigration/src/ccmigration/accountmove.py", line 316, in _set_move_line
    raise KeyError("Tax code '%s' not found even in the mapping" % line.tax_code_id.name)
KeyError: "Tax code 'Ritenuta 20% Base' not found even in the mapping"

Ritenuta acconto
13,73%

transoportion Reso riparazione in garanzia

resa PORTO FRANCO TNT C/ABB. n°3369931

