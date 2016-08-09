# -*- coding: utf-8 -*-
from .base import BaseCommand

# ------------------------------------------------
# [CGM] One2Many fields
# - line_id
# - line_partial_ids
# ------------------------------------------------
# [CGM] Fields in destination but not in source
# - __last_update
# - create_uid
# - display_name
# - id
# - opening_reconciliation
# - write_date
# - write_uid

class AccountMoveReconcileMigration(BaseCommand):

    _default_values = {
        # [CGM] Add any value shared by all instances of the model.
        #       Normally, fields like 'company_id' o 'currency_id' are good
        #       candidates.
    }

    _fields = {
        'create_date': None,
        'name': None,
        'type': None,
        'x_uuid': None
    }

    def check_existent(self, record):
        """Search for duplicated records eg. for res.partner model.
        """
        return self.dest_model.search([
                ('x_uuid', '=', record['x_uuid']),
            ],
            context=self.default_context
        )

    def get_migration_data(self):
        self.source_model = self.source.AccountMoveReconcile
        self.dest_model = self.destination.AccountMoveReconcile

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

