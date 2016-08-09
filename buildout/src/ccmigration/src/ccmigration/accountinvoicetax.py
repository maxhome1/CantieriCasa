# -*- coding: utf-8 -*-
from .base import BaseCommand

# ------------------------------------------------
# [CGM] Fields in destination but not in source
# - __last_update
# - account_analytic_id
# - create_date
# - create_uid
# - display_name
# - id
# - write_date
# - write_uid

class AccountInvoiceTaxMigration(BaseCommand):

    _default_values = {
        # [CGM] Add any value shared by all instances of the model.
        #       Normally, fields like 'company_id' o 'currency_id' are good
        #       candidates.
    }

    _fields = {
        'amount': None,
        'base': None,
        'base_amount': None,
        'factor_base': None,
        'factor_tax': None,
        'manual': None,
        'name': None,
        'sequence': None,
        'tax_amount': None,
        'account_id': {
              'name': 'account_id',
              'type': 'many2one',
              'relation': 'account.account',
              'create': False # [CGM] Change to True if needed
        },
        'base_code_id': {
              'name': 'base_code_id',
              'type': 'many2one',
              'relation': 'account.tax.code',
              'create': False # [CGM] Change to True if needed
        },
        'company_id': {
              'name': 'company_id',
              'type': 'many2one',
              'relation': 'res.company',
              'create': False # [CGM] Change to True if needed
        },
        'invoice_id': {
              'name': 'invoice_id',
              'type': 'many2one',
              'relation': 'account.invoice',
              'create': False # [CGM] Change to True if needed
        },
        'tax_code_id': {
              'name': 'tax_code_id',
              'type': 'many2one',
              'relation': 'account.tax.code',
              'create': False # [CGM] Change to True if needed
        },
    }

    def get_migration_data(self):
        self.source_model = self.source.AccountInvoiceTax
        self.dest_model = self.destination.AccountInvoiceTax

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

