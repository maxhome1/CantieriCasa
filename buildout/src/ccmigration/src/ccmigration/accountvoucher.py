# -*- coding: utf-8 -*-
from .base import BaseCommand

# ------------------------------------------------
# [CGM] One2Many fields
# - line_cr_ids
# - line_dr_ids
# - line_ids
# - move_ids
# ------------------------------------------------
# [CGM] Fields in source but not in destination
# - x_uuid
# ------------------------------------------------
# [CGM] Fields in destination but not in source
# - __last_update
# - create_date
# - create_uid
# - currency_help_label
# - display_name
# - id
# - is_multi_currency
# - message_follower_ids
# - message_ids
# - message_is_follower
# - message_last_post
# - message_summary
# - message_unread
# - paid
# - paid_amount_in_company_currency
# - payment_rate
# - payment_rate_currency_id
# - write_date
# - write_uid

def lookup_for_move_line(value):
    return [
        ('x_uuid', '=', value.x_uuid),
    ]

class AccountVoucherMigration(BaseCommand):

    _default_values = {
        # [CGM] Add any value shared by all instances of the model.
        #       Normally, fields like 'company_id' o 'currency_id' are good
        #       candidates.
        'company_id': 1,
        'currency_id': 1,
    }

    _fields = {
        'amount': None,
        'audit': None,
        'comment': None,
        'date': None,
        'date_due': None,
        'name': None,
        'narration': None,
        'number': None,
        'pay_now': None,
        'payment_option': None,
        'pre_line': None,
        'reference': None,
        'state': None,
        'tax_amount': None,
        'type': None,
        'writeoff_amount': None,
        'x_uuid': None,
        'account_id': {
              'name': 'account_id',
              'type': 'many2one',
              'relation': 'account.account',
              'create': False # [CGM] Change to True if needed
        },
        # [CGM] The following field has no relations and
        #       can be commented out.
        # 'analytic_id': {
        #       'name': 'analytic_id',
        #       'type': 'many2one',
        #       'relation': 'account.analytic.account',
        #       'create': False # [CGM] Change to True if needed
        # },
        'journal_id': {
              'unique_field': 'code',
              'name': 'journal_id',
              'type': 'many2one',
              'relation': 'account.journal',
              'create': False # [CGM] Change to True if needed
        },
        'move_id': {
              'unique_field': 'x_uuid',
              'name': 'move_id',
              'type': 'many2one',
              'relation': 'account.move',
              'create': False # [CGM] Change to True if needed
        },
        'partner_id': {
              'name': 'partner_id',
              'type': 'many2one',
              'relation': 'res.partner',
              'create': False # [CGM] Change to True if needed
        },
        'period_id': {
              'name': 'period_id',
              'type': 'many2one',
              'relation': 'account.period',
              'create': False # [CGM] Change to True if needed
        },
        'tax_id': {
              'name': 'tax_id',
              'type': 'many2one',
              'relation': 'account.tax',
              'create': False # [CGM] Change to True if needed
        },
        # [CGM] The following field has no relations and
        #       can be commented out.
        # 'writeoff_acc_id': {
        #       'name': 'writeoff_acc_id',
        #       'type': 'many2one',
        #       'relation': 'account.account',
        #       'create': False # [CGM] Change to True if needed
        # },
        'line_cr_ids': {
            'type': 'custom',
            'setter': '_set_line_cr_ids'
        },
        'line_dr_ids': {
            'type': 'custom',
            'setter': '_set_line_dr_ids'
        },
        'move_ids': {
            'type': 'custom',
            'setter': '_set_move_ids'
        }
    }

    def _set_move_ids(self, old, new):
        move_ids = getattr(old, 'move_ids')
        if len(move_ids) == 0:
            return

        moveline_ids = []
        for moveline in move_ids:
            id_ = self.destination.AccountMoveLine.search(
                [('x_uuid', '=', moveline.x_uuid)],
                context=self.default_context
            )
            if len(id_) != 1:
                if self.config['debug']:
                    print "Moveline with no x_uuid, continue"
                else:
                    raise KeyError("Moveline not found: {}".format(moveline.name))
            else:
                moveline_ids.append(id_[0])
        new['move_ids'] = [(6, 0, moveline_ids)]

    def _set_line(self, old, new, field_name):
        line_ids = getattr(old, field_name)
        if len(line_ids) == 0:
            return

        fields = [
            'amount',
            'amount_original',
            'amount_unreconciled',
            'date_due',
            'date_original',
            'name',
            'type',
            'untax_amount',
        ]

        new_lines = []
        for line in line_ids:
            new_line = {
                'company_id': 1
            }
            for field in fields:
                value = getattr(line, field)
                if value is not None:
                    new_line[field] = value

            self._set_value_for_line(
                line,
                new_line,
                'account_analytic_id',
                'AccountAnalyticAccount'
            )
            self._set_value_for_line(
                line,
                new_line,
                'account_id',
                'AccountAccount'
            )
            self._set_value_for_line(
                line,
                new_line,
                'move_line_id',
                'AccountMoveLine',
                lookup=lookup_for_move_line
            )
            self._set_value_for_line(
                line,
                new_line,
                'partner_id',
                'ResPartner'
            )
            new_lines.append((0, 0, new_line))

        new[field_name] = new_lines

    def _set_line_cr_ids(self, new, old):
        self._set_line(new, old, 'line_cr_ids')

    def _set_line_dr_ids(self, new, old):
        self._set_line(new, old, 'line_dr_ids')

    def check_existent(self, record):
        """Search for duplicated records eg. for res.partner model.
        """
        return self.dest_model.search([
                ('x_uuid', '=', record['x_uuid']),
            ],
            context=self.default_context
        )

    def get_migration_data(self):
        self.source_model = self.source.AccountVoucher
        self.dest_model = self.destination.AccountVoucher

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

    def migrate(self):
        super(AccountVoucherMigration, self).migrate()
        self.get_migration_data()

        n_total = len(self.source_data)
        for index, old in enumerate(self.source_data, 1):
            print u"[{}/{}] Setting state '{}'".format(
                index,
                n_total,
                old.state
            )
            new = self.destination.AccountVoucher.browse([
                ('x_uuid', '=', old.x_uuid)
            ])[0]
            new.state = old.state
