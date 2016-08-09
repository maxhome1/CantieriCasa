# -*- coding: utf-8 -*-
from .base import BaseCommand


class ProductPricelistMigration(BaseCommand):
    """Product Pricelist migration from Openerp 6 to Odoo 8
    """

    _fields = {
        'name': None,
        'company_id': None,
        'version_id':  {
            "type": "custom",
            "setter": "_get_versions"
        },
        'currency_id': None,
        'active': None,
        'type': None
    }

    def get_migration_data(self):
        """Partner migration data:

        * source_model: Odoo 6 - product.pricelist
        * dest_model: Odoo 8 - product.pricelist
        * source_model_ids: all category ids
        * source_data: all category objects
        """
        self.source_model = self.source.ProductPricelist
        self.dest_model = self.destination.ProductPricelist

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

    def _get_versions(self, old, new):
        version_id = old.version_id
        if len(version_id) == 0:
            return

        fields = [
            "active",
            "date_end",
            "date_start",
            "name"
        ]

        new_lines = []
        for line in version_id:
            new_line = {}
            for field in fields:
                value = getattr(line, field)
                if value is not None:
                    new_line[field] = value
            new_lines.append((0, 0, new_line))

        new["version_id"] = new_lines
