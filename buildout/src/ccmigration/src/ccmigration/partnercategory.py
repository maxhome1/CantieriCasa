# -*- coding: utf-8 -*-
from .base import BaseCommand


class PartnerCategoryMigration(BaseCommand):
    """Partner category migration from Openerp 6 to Odoo 8
    """

    _fields = {
        "active": None,
        "name": None,
        # "parent_id": None
    }

    def get_migration_data(self):
        """Partner migration data:

        * source_model: Odoo 6 - res.partner.category
        * dest_model: Odoo 8 - res.partner.category
        * source_model_ids: all category ids
        * source_data: all category objects
        """
        self.source_model = self.source.ResPartnerCategory
        self.dest_model = self.destination.ResPartnerCategory

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

    def migrate(self):
        super(PartnerCategoryMigration, self).migrate()
        # Set parent_id
        for el in self.source_data:
            parent = el.parent_id
            if not parent:
                continue

            cat_id = self.dest_model.search(
                [('name', '=', el.name)],
                context=self.default_context
            )
            parent_id = self.dest_model.search(
                [('name', '=', parent.name)],
                context=self.default_context
            )
            self.dest_model.write(cat_id, {'parent_id': parent_id[0]})
