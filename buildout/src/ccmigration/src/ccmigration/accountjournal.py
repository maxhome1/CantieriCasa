# -*- coding: utf-8 -*-
from .base import BaseCommand
from .settings import ACCOUNT_MAPPING

# ------------------------------------------------
# [CGM] Fields in source but not in destination
# - internal_sequence_id
# - refund_journal
# - view_id
# ------------------------------------------------
# [CGM] Fields in destination but not in source
# - __last_update
# - cash_control
# - cashbox_line_ids
# - create_date
# - create_uid
# - display_name
# - id
# - internal_account_id
# - loss_account_id
# - profit_account_id
# - with_last_closing_balance
# - write_date
# - write_uid

# [{'id': 18, 'name': 'Apertura stato patrimoniale', 'update_posted': True},
#  {'id': 8, 'name': 'Contante', 'update_posted': False},
#  {'id': 9, 'name': 'Banca', 'update_posted': False},
#  {'id': 22, 'name': 'Cash', 'update_posted': True},
#  {'id': 23, 'name': 'Banca Popolare del Lazio', 'update_posted': True},
#  {'id': 10, 'name': 'BNL', 'update_posted': True},
#  {'id': 19, 'name': 'PAYPAL', 'update_posted': True},
#  {'id': 21, 'name': 'BPFondi', 'update_posted': True},
#  {'id': 15, 'name': 'Chiusura conto economico', 'update_posted': True},
#  {'id': 17, 'name': 'Chiusura patrimoniale', 'update_posted': True},
#  {'id': 5,
#   'name': 'Sezionale Note di Credito Fornitori',
#   'update_posted': False},
#  {'id': 3, 'name': 'Sezionale Acquisti', 'update_posted': False},
#  {'id': 6, 'name': 'Sezionali vari', 'update_posted': False},
#  {'id': 12, 'name': 'Note di Credito', 'update_posted': True},
#  {'id': 14, 'name': 'Note di Debito', 'update_posted': True},
#  {'id': 7, 'name': 'Sezionale delle voci di apertura', 'update_posted': False},
#  {'id': 2, 'name': 'Sezionale Vendite', 'update_posted': False},
#  {'id': 4, 'name': 'Sezionale Note di Credito', 'update_posted': False},
#  {'id': 1, 'name': 'Stock Journal', 'update_posted': False},
#  {'id': 20, 'name': 'Transitorio', 'update_posted': True},
#  {'id': 16, 'name': 'Utile e perdita di esercizio', 'update_posted': True},
#  {'id': 24, 'name': 'carta di credito MPS', 'update_posted': True},
#  {'id': 11, 'name': 'Giornale di chiusura 2010', 'update_posted': True},
#  {'id': 13, 'name': 'Paghe e contributi', 'update_posted': True}]


def resolve_account(account):
    value = ACCOUNT_MAPPING.get(account.strip())
    return value or account

class AccountJournalMigration(BaseCommand):

    # currency is actually 1, but we have to force to keep it aligned
    # with the accounts
    _default_values = {
        'currency': False,
    }

    _fields = {
        'allow_date': None,
        'centralisation': None,
        'code': None,
        'entry_posted': None,
        'group_invoice_lines': None,
        'name': None,
        'type': None,
        'update_posted': None,
        # [CGM] The following field has no relations and
        #       can be commented out.
        # 'account_control_ids': {
        #       'name': 'account_control_ids',
        #       'type': 'many2many',
        #       'relation': 'account.account',
        #       'create': False # [CGM] Change to True if needed
        # },
        'analytic_journal_id': {
              'name': 'analytic_journal_id',
              'type': 'many2one',
              'relation': 'account.analytic.journal',
              'create': False # [CGM] Change to True if needed
        },
        'default_credit_account_id': {
              'name': 'default_credit_account_id',
              'type': 'many2one',
              'relation': 'account.account',
              'create': False, # [CGM] Change to True if needed
              'transform': resolve_account
        },
        'default_debit_account_id': {
              'name': 'default_debit_account_id',
              'type': 'many2one',
              'relation': 'account.account',
              'create': False, # [CGM] Change to True if needed
              'transform': resolve_account
        },
        # [CGM] The following field has no relations and
        #       can be commented out.
        # 'groups_id': {
        #       'name': 'groups_id',
        #       'type': 'many2many',
        #       'relation': 'res.groups',
        #       'create': False # [CGM] Change to True if needed
        # },
        'sequence_id': {
              'name': 'sequence_id',
              'type': 'many2one',
              'relation': 'ir.sequence',
              'create': False # [CGM] Change to True if needed
        },
        # [CGM] The following field has no relations and
        #       can be commented out.
        # 'type_control_ids': {
        #       'name': 'type_control_ids',
        #       'type': 'many2many',
        #       'relation': 'account.account.type',
        #       'create': False # [CGM] Change to True if needed
        # },
        'user_id': {
            'type': 'custom',
            'setter': 'set_user_id'
        },
    }

    def get_migration_data(self):
        self.source_model = self.source.AccountJournal
        self.dest_model = self.destination.AccountJournal

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

        def check_existent(self, record):
            """Search for duplicated records eg. for res.partner model.
            """
            return self.dest_model.search([
                    'code = {}'.format(record['code'])
                ],
                context=self.default_context
            )

        codes = [
            'ASP',
            'BNK5',
            'BNK6',
            'CCE',
            'clj',
            'CP',
            'NC',
            'ND',
            'pagco',
            'UPE',

            'TRANS',
            'BNK7',
            'carta',
            'BNK4',
            'BNK3',
        ]
        self.source_model_ids = self.source_model.search(
            [('code', 'in', codes)],
            order='id',
            limit=self.config['limit'],
            offset=self.config['offset'],
            context=self.default_context
        )
        if self.source_model_ids:
            self.source_data = self.source_model.browse(self.source_model_ids)

