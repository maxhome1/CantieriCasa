# -*- coding: utf-8 -*-
from .base import BaseCommand


class UomMigration(BaseCommand):
    """UOM migration from Openerp 6 to Odoo 8
    """

    _fields = {
        "active": None,
        "name": None,
        "factor": None,
        'factor_inv': None,
        "rounding": None,
        "uom_type": None,
        "category_id": {
            "name": "category_id",
            "type": "m2o",
            "relation": "product.uom.categ",
            "create": True
        }
    }


    def get_migration_data(self):
        """Partner migration data:

        * source_model: Odoo 6 - product.uom
        * dest_model: Odoo 8 - product.uom
        * source_model_ids: all uom ids
        * source_data: all uom objects
        """
        self.source_model = self.source.ProductUom
        self.dest_model = self.destination.ProductUom

        self.source_model_ids = self.source_model.search(
            [],
            order='id',
            limit=self.config['limit'],
            offset=self.config['offset'],
            context=self.default_context
        )
        if not self.source_model_ids:
            self.source_data = []
        else:
            self.source_data = self.source_model.browse(self.source_model_ids)
