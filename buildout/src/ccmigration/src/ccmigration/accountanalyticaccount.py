# -*- coding: utf-8 -*-
from .base import BaseCommand

# ------------------------------------------------
# [CGM] One2Many fields
# - child_ids
# - line_ids
# ------------------------------------------------
# [CGM] Fields in source but not in destination
# - amount_invoiced
# - amount_max
# - contact_id
# - pricelist_id
# - to_invoice
# ------------------------------------------------
# [CGM] Fields in destination but not in source
# - __last_update
# - company_uom_id
# - create_date
# - create_uid
# - display_name
# - id
# - manager_id
# - message_follower_ids
# - message_ids
# - message_is_follower
# - message_last_post
# - message_summary
# - message_unread
# - template_id
# - use_tasks
# - write_date
# - write_uid

class AccountAnalyticAccountMigration(BaseCommand):

    _default_values = {
        'company_id': 1,
        'currency_id': 1
    }

    _fields = {
        'balance': None,
        'code': None,
        'complete_name': None,
        'credit': None,
        'date': None,
        'date_start': None,
        'debit': None,
        'description': None,
        'name': None,
        'quantity': None,
        'quantity_max': None,
        'state': None,
        'type': None,
        'partner_id': {
              'name': 'partner_id',
              'type': 'many2one',
              'relation': 'res.partner',
              'create': False # [CGM] Change to True if needed
        },
        'user_id': {
            'type': 'custom',
            'setter': 'set_user_id'
        },
    }

    def get_migration_data(self):
        self.source_model = self.source.AccountAnalyticAccount
        self.dest_model = self.destination.AccountAnalyticAccount

        self.source_data = []

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
        super(AccountAnalyticAccountMigration, self).migrate()

        print "Setting parent id"
        for el in self.source_data:
            parent = el.parent_id
            if not parent:
                continue

            id_ = self.dest_model.search([
                    ('name', '=', el.name),
                ],
                context=self.default_context
            )
            parent_id = self.dest_model.search([
                    ('name', '=', parent.name),
                ],
                context=self.default_context
            )
            self.dest_model.write(id_, {'parent_id': parent_id[0]})

