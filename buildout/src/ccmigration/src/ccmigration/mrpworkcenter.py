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

class MrpWorkcenterMigration(BaseCommand):

    _default_values = {
        # [CGM] Add any value shared by all instances of the model.
        #       Normally, fields like 'company_id' o 'currency_id' are good
        #       candidates.
        'company_id': 1,

    }

    _fields = {
        'active': None,
        'capacity_per_cycle': None,
        'code': None,
        'costs_cycle': None,
        'costs_hour': None,
        'name': None,
        'note': None,
        'resource_type': None,
        'time_cycle': None,
        'time_efficiency': None,
        'time_start': None,
        'time_stop': None,
        'calendar_id': {
              'name': 'calendar_id',
              'type': 'many2one',
              'relation': 'resource.calendar',
              'create': False # [CGM] Change to True if needed
        },
        'costs_cycle_account_id': {
              'name': 'costs_cycle_account_id',
              'type': 'many2one',
              'relation': 'account.analytic.account',
              'create': True # [CGM] Change to True if needed
        },
        'costs_general_account_id': {
              'name': 'costs_general_account_id',
              'type': 'many2one',
              'relation': 'account.account',
              'create': False # [CGM] Change to True if needed
        },
        'costs_hour_account_id': {
              'name': 'costs_hour_account_id',
              'type': 'many2one',
              'relation': 'account.analytic.account',
              'create': True # [CGM] Change to True if needed
        },
        'costs_journal_id': {
              'name': 'costs_journal_id',
              'type': 'many2one',
              'relation': 'account.analytic.journal',
              'create': True # [CGM] Change to True if needed
        },
        'product_id': {
              'name': 'product_id',
              'type': 'many2one',
              'relation': 'product.product',
              'create': False # [CGM] Change to True if needed
        },
        'resource_id': {
              'name': 'resource_id',
              'type': 'many2one',
              'relation': 'resource.resource',
              'create': False # [CGM] Change to True if needed
        },
        # [CGM] The following field has no relations and
        #       can be commented out.
        'user_id': {
            'type': 'custom',
            'setter': 'set_user_id'
        },
    }

    def build_record(self, *args, **kwargs):
        record = super(MrpWorkcenterMigration, self).build_record(*args, **kwargs)
        # New constraint in odoo
        if record['capacity_per_cycle'] == 0:
            record['capacity_per_cycle'] = 1.0
        return record

    def get_migration_data(self):
        self.source_model = self.source.MrpWorkcenter
        self.dest_model = self.destination.MrpWorkcenter

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
            [],
            order='id',
            limit=self.config['limit'],
            offset=self.config['offset'],
            context=self.default_context
        )
        if self.source_model_ids:
            self.source_data = self.source_model.browse(self.source_model_ids)

