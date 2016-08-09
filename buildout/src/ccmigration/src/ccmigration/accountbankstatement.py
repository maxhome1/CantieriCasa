# -*- coding: utf-8 -*-
from .base import BaseCommand

# ------------------------------------------------
# [CGM] One2Many fields
# - line_ids
# - move_line_ids
# ------------------------------------------------
# [CGM] Fields in source but not in destination
# - balance_end_cash
# - ending_details_ids
# - starting_details_ids
# ------------------------------------------------
# [CGM] Fields in destination but not in source
# - __last_update
# - all_lines_reconciled
# - cash_control
# - closing_details_ids
# - create_date
# - create_uid
# - details_ids
# - difference
# - display_name
# - id
# - last_closing_balance
# - message_follower_ids
# - message_ids
# - message_is_follower
# - message_last_post
# - message_summary
# - message_unread
# - opening_details_ids
# - write_date
# - write_uid

class AccountBankStatementMigration(BaseCommand):

    _default_values = {
        # [CGM] Add any value shared by all instances of the model.
        #       Normally, fields like 'company_id' o 'currency_id' are good
        #       candidates.
        'company_id': 1,
        'currency': 1,
    }

    _fields = {
        'balance_end': None,
        'balance_end_real': None,
        'balance_start': None,
        'closing_date': None,
        'date': None,
        'name': None,
        'state': None,
        'total_entry_encoding': None,
        'account_id': {
              'unique_field': 'code',
              'name': 'account_id',
              'type': 'many2one',
              'relation': 'account.account',
              'create': False # [CGM] Change to True if needed
        },
        'journal_id': {
              'unique_field': 'code',
              'name': 'journal_id',
              'type': 'many2one',
              'relation': 'account.journal',
              'create': False # [CGM] Change to True if needed
        },
        'period_id': {
              'name': 'period_id',
              'type': 'many2one',
              'relation': 'account.period',
              'create': False # [CGM] Change to True if needed
        },
        'user_id': {
              'type': 'custom',
              'setter': 'set_user_id'
        },
    }

    def get_migration_data(self):
        self.source_model = self.source.AccountBankStatement
        self.dest_model = self.destination.AccountBankStatement

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

