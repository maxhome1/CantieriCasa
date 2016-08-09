# -*- coding: utf-8 -*-
from .base import BaseCommand


class ProductCategoryMigration(BaseCommand):
    """Product category migration from Openerp 6 to Odoo 8
    """

        # ['child_id',
        #  'complete_name',
        #  'name',
        #  'parent_id',
        #  'property_account_expense_categ',
        #  'property_account_income_categ',
        #  'property_stock_account_input_categ',
        #  'property_stock_account_output_categ',
        #  'property_stock_journal',
        #  'property_stock_variation',
        #  'sequence',
        #  'type']
    _fields = {
        'complete_name': None,
        'name': None,
        # 'property_account_expense_categ',
        # 'property_account_income_categ',
        # 'property_stock_account_input_categ',
        # 'property_stock_account_output_categ',
        # 'property_stock_journal',
        # 'property_stock_variation',
        'sequence': None,
        'type': None
    }

    def get_migration_data(self):
        """Partner migration data:

        * source_model: Odoo 6 - product.category
        * dest_model: Odoo 8 - product.category
        * source_model_ids: all category ids
        * source_data: all category objects
        """
        self.source_model = self.source.ProductCategory
        self.dest_model = self.destination.ProductCategory

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

    def check_existent(self, record):
        """Search for duplicated records eg. for res.partner model.
        """
        return self.dest_model.search([
                '&',
                ('name', '=', record['name']),
                ('sequence', '=', record['sequence'])
            ],
            context=self.default_context
        )

    def migrate(self):
        super(ProductCategoryMigration, self).migrate()
        # Set parent_id
        print "Setting parent id"
        for el in self.source_data:
            parent = el.parent_id
            if not parent:
                continue

            cat_id = self.dest_model.search([
                    '&',
                    ('name', '=', el.name),
                    ('sequence', '=', el.sequence)
                ],
                context=self.default_context
            )
            parent_id = self.dest_model.search([
                    '&',
                    ('name', '=', parent.name),
                    ('sequence', '=', parent.sequence)
                ],
                context=self.default_context
            )
            self.dest_model.write(cat_id, {'parent_id': parent_id[0]})
