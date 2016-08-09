# -*- coding: utf-8 -*-
from .base import BaseCommand
from .address import AddressMixin


class PartnerMigration(BaseCommand, AddressMixin):
    """Partner migration from Openerp 6 to Odoo 8
    """

    _fields = {
        "active": None,
        "address": {
            "type": "custom",
            "setter": "get_address"
        },
        "birth_date": {"name": "birthdate"},
        "carriage_condition_id": {
            "name": "carriage_condition_id",
            "type": "m2o",
            "relation": "stock.picking.carriage_condition",
            "create": True # Pretty simple model
        },
        "category_id": {
            "name": "category_id",
            "type": "m2m",
            "relation": "res.partner.category",
            "create": False  # partner_category command creates these records
        },
        "city": None,
        "comment": None,
        "company_id": {
            "name": "company_id",
            "type": "m2o",
            "relation": "res.company",
            "create": False
        },
        "country": {
            "name": "country_id",
            "type": "m2o",
            "relation": "res.country",
            "create": False
        },
        "credit": None,
        "credit_limit": None,
        "customer": None,
        "date": None,
        "debit": None,
        "debit_limit": None,
        "ean13": None,
        "email": None,
        "employee": None,
        "fiscalcode": None,
        "goods_description_id": {
            "name": "goods_description_id",
            "type": "m2o",
            "relation": "stock.picking.goods_description",
            "create": True # Pretty simple model
        },
        "lang": None,
        "last_reconciliation_date": None,
        "mobile": None,
        "name": None,
        "parent_id": {
            "type": "custom",
            "setter": "_set_parent_id"
        },
        "phone": None,
        'property_account_payable': {
            'unique_field': 'code',
            'name': 'property_account_payable',
            'type': 'many2one',
            'relation': 'account.account',
            'create': False # [CGM] Change to True if needed
        },
        'property_account_position': {
            'unique_field': 'code',
            'name': 'property_account_position',
            'type': 'many2one',
            'relation': 'account.fiscal.position',
            'create': False # [CGM] Change to True if needed
        },
        'property_account_receivable': {
            'unique_field': 'code',
            'name': 'property_account_receivable',
            'type': 'many2one',
            'relation': 'account.account',
            'create': False # [CGM] Change to True if needed
        },
        "property_payment_term": {
            "name": "property_payment_term",
            "type": "m2o",
            "relation": "account.payment.term",
            "create": False
        },
        "property_product_pricelist": {
            "name": "property_product_pricelist",
            "type": "m2o",
            "relation": "product.pricelist",
            "create": False # Created by productpricelist
        },
        "property_product_pricelist_purchase": {
            "name": "property_product_pricelist_purchase",
            "type": "m2o",
            "relation": "product.pricelist",
            "create": False # Created by productpricelist
        },
        "property_stock_customer": {
            "name": "property_stock_customer",
            "type": "m2o",
            "relation": "stock.location",
            "create": True
        },
        "property_stock_supplier": {
            "name": "property_stock_supplier",
            "type": "m2o",
            "relation": "stock.location",
            "create": True
        },
        "ref": None,
        "ref_companies": None,
        # Not migrated
        # 'section_id': {
        #       'name': 'section_id',
        #       'type': 'many2one',
        #       'relation': 'crm.case.section',
        #       'create': False # [CGM] Change to True if needed
        # },
        "supplier": None,
        "title": {
            "name": "title",
            "type": "m2o",
            "relation": "res.partner.title",
            "create": True
        },
        'transportation_reason_id': {
              'name': 'transportation_reason_id',
              'type': 'many2one',
              'relation': 'stock.picking.transportation_reason',
              'create': False # [CGM] Change to True if needed
        },
        'user_id': {
            'type': 'custom',
            'setter': '_set_user_id',
        },
        "vat": None,
        "vat_subjected": None,
        "website": None
    }

    def _set_user_id(self, old, new):
        self.set_user_id(old, new, force_admin=False)
        # We'll handle the new 'is_company' flag here
        company_acronyms = (
            ' srl', ' s.r.l.',
            ' snc', ' s.n.c.',
            ' spa', ' s.p.a.',
            ' sas', ' s.a.s',

        )
        for acronym in company_acronyms:
            if acronym in old.name.lower():
                new['is_company'] = True

    def _set_parent_id(self, old, new):
        old_parent = old.parent_id
        if not old_parent:
            return

        parent = self.destination.ResPartner.search(
            [
                '&',
                ('name', '=', old_parent.name),
                ('vat', '=', old_parent.vat)
            ],
            context=self.default_context)

        if len(parent) != 1:
            if self.config['debug']:
                print "Error %s not found" % old_parent.name
            else:
                raise KeyError("Multiple partners or partner not found")
        else:
            new['parent_id'] = parent[0]

    def check_existent(self, record):
        return self.dest_model.search(
            ['&', ('name', '=', record['name']), ('vat', '=', record['vat'])],
            context=self.default_context)

    def get_migration_data(self):
        """Partner migration data:

        * source_model: Odoo 6 - res.partner
        * dest_model: Odoo 8 - res.partner
        * source_model_ids: all partner ids not related to a user
                            and that are not company
        * source_data: partner objects
        """
        self.source_model = self.source.ResPartner
        self.dest_model = self.destination.ResPartner

        self.source_model_ids = self.source_model.search([],
            order='parent_id desc, id',
            context=self.default_context,
            limit=self.config['limit'],
            offset=self.config['offset'],
        )

        if not self.source_model_ids:
            self.source_data = []
        else:
            self.source_data = self.source_model.browse(self.source_model_ids)

    def get_address(self, old, new):

        default_address = [i for i in old.address if i.type in ('default', False)]
        if len(default_address) > 1:
            print "Too many default address for partner {}".format(
                default_address[0].partner_id.name
            )
            print "I will get the first one"
            new.update(self.get_address_value(default_address[0]))
