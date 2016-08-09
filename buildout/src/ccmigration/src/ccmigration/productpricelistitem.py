# -*- coding: utf-8 -*-
from .base import BaseCommand

# ------------------------------------------------
# [CGM] Fields in destination but not in source
# - __last_update
# - create_date
# - create_uid
# - display_name
# - id
# - write_date
# - write_uid

class ProductPricelistItemMigration(BaseCommand):

    _ignore_to_many_values = True

    _default_values = {
        # [CGM] Add any value shared by all instances of the model.
        #       Normally, fields like 'company_id' o 'currency_id' are good
        #       candidates.
        'company_id': 1,
    }

    _fields = {
        'base': None,
        'min_quantity': None,
        'name': None,
        'price_discount': None,
        'price_max_margin': None,
        'price_min_margin': None,
        'price_round': None,
        'price_surcharge': None,
        'sequence': None,
        # [CGM] The following field has no relations and
        #       can be commented out.
        # 'base_pricelist_id': {
        #       'name': 'base_pricelist_id',
        #       'type': 'many2one',
        #       'relation': 'product.pricelist',
        #       'create': False # [CGM] Change to True if needed
        # },
        'categ_id': {
              'name': 'categ_id',
              'type': 'many2one',
              'relation': 'product.category',
              'create': False # [CGM] Change to True if needed
        },
        # 'company_id': {
        #       'name': 'company_id',
        #       'type': 'many2one',
        #       'relation': 'res.company',
        #       'create': False # [CGM] Change to True if needed
        # },
        'price_version_id': {
            # 'type': 'custom',
            # 'setter': '_set_price_version_id'
              'name': 'price_version_id',
              'type': 'many2one',
              'relation': 'product.pricelist.version',
              'create': False # [CGM] Change to True if needed
        },
        'product_id': {
              'name': 'product_id',
              'type': 'many2one',
              'relation': 'product.product',
              'create': False # [CGM] Change to True if needed
        },
        # [CGM] The following field has no relations and
        #       can be commented out.
        # 'product_tmpl_id': {
        #       'name': 'product_tmpl_id',
        #       'type': 'many2one',
        #       'relation': 'product.template',
        #       'create': False # [CGM] Change to True if needed
        # },
    }

    # def _set_price_version_id(self, old, new):
    #     price_version_id = old.price_version_id
    #     if not price_version_id:
    #         return
    #
    #     fields = [
    #         "active",
    #         "date_end",
    #         "date_start",
    #         "name"
    #     ]
    #     new_line = {}
    #     for field in fields:
    #         value = getattr(price_version_id, field)
    #         if value is not None:
    #             new_line[field] = value
    #     pricelist_id = self.destination.ProductPricelist.search(
    #         [('name', '=', price_version_id.pricelist_id.name)],
    #         context=self.default_context
    #     )
    #     new_line['pricelist_id'] = pricelist_id[0]
    #     id_ = self.destination.ProductPricelistVersion.create(new_line)
    #     new["price_version_id"] = id_

    def get_migration_data(self):
        self.source_model = self.source.ProductPricelistItem
        self.dest_model = self.destination.ProductPricelistItem

        self.source_data = []

        # [CGM] If you need to narrow differently the query when the script is
        #       run in debug mode, de-comment the code below and change the
        #       seach parameters accordingly.
        #       By default, all objects are returned.

        # if self.config['debug']:
        #     self.source_model_ids = self.source_model.search(
        #         [],
        #         order='id',
        #         limit=self.config['limit'],
        #         offset=self.config['offset'],
        #         context=self.default_context
        #     )
        # else:
        #     self.source_model_ids = self.source_model.search(
        #         [],
        #         order='id',
        #         limit=self.config['limit'],
        #         offset=self.config['offset'],
        #         context=self.default_context
        #     )

        self.source_model_ids = self.source_model.search(
            [
                ('price_version_id.name!="Casa 48\'HT 2012 rev.01"'),
                ('price_version_id.name!="Rimessaggio Imbarcazioni 2013-2014"')
            ],
            order='id',
            limit=self.config['limit'],
            offset=self.config['offset'],
            context=self.default_context
        )
        if self.source_model_ids:
            self.source_data = self.source_model.browse(self.source_model_ids)

