# -*- coding: utf-8 -*-
from .base import BaseCommand


# IMPORTANT Launch this migration with debug option

class ProductSupplierinfoMigration(BaseCommand):
    """ProductSupplierinfo migration from Openerp 6 to Odoo 8
    """
    _fields = {
        'delay': None,
        'min_qty': None,
        'name': {
            'name': 'name',
            'type': 'm2o',
            'relation': 'res.partner',
            'create': False
        },
        'pricelist_ids': {
            'type': 'custom',
            'setter': '_set_pricelist_ids'
        },
        'product_code': None,
        'product_id': {
            'type': 'custom',
            'setter': '_set_product_id'
        },
        'product_name': None,
        'product_uom': {
            'name': 'product_uom',
            'type': 'm2o',
            'relation': 'product.uom',
            'create': False
        },
        'qty': None,
        'sequence': None
    }

    def _set_pricelist_ids(self, old, new):
        pricelist_ids = old.pricelist_ids
        if len(pricelist_ids) == 0:
            return

        fields = [
            "min_quantity",
            "price",
            "name",
        ]

        new_lines = []
        for line in pricelist_ids:
            new_line = {}
            for field in fields:
                value = getattr(line, field)
                if value is not None:
                    new_line[field] = value
            new_lines.append((0, 0, new_line))

        new["pricelist_ids"] = new_lines

    def _set_product_id(self, old, new):
        product_id = old.product_id
        if not product_id:
            return
        product_tmpl_id = self.destination.ProductTemplate.search(
            [('name', '=', product_id.name)],
            context = self.default_context
        )
        if len(product_tmpl_id) == 1:
            new['product_tmpl_id'] = product_tmpl_id[0]

    def check_existent(self, record):
        """Search for duplicated records eg. for res.partner model.
        """
        # This will skip a record that has no product associated (an error
        # from the old db)
        if not 'product_tmpl_id' in record:
            return True
        return self.dest_model.search([
                '&',
                ('name', '=', record['name']),
                ('product_tmpl_id', '=', record['product_tmpl_id']),
            ],
            context=self.default_context
        )

    def build_record(self, el, fast=False, force_fast_fields=['name']):
        return super(ProductSupplierinfoMigration, self).build_record(
            el, fast, force_fast_fields=['name', 'product_id'])


    def get_migration_data(self):
        """ProductSupplierInfo migration data:

        * source_model: Odoo 6 - product.supplierinfo
        * dest_model: Odoo 8 - product.supplierinfo
        * source_model_ids: all bank ids
        * source_data: partner objects
        """
        self.source_model = self.source.ProductSupplierinfo
        self.dest_model = self.destination.ProductSupplierinfo
        self.source_model_ids = self.source_model.search(
            [],
            order='id',
            context=self.default_context,
            limit=self.config['limit'],
            offset=self.config['offset']
        )

        if not self.source_model_ids:
            self.source_data = []
        else:
            self.source_data = self.source_model.browse(self.source_model_ids)
