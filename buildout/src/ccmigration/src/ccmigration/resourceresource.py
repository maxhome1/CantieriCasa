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

class ResourceResourceMigration(BaseCommand):

    _default_values = {
        # [CGM] Add any value shared by all instances of the model.
        #       Normally, fields like 'company_id' o 'currency_id' are good
        #       candidates.
        'company_id': 1,
    }

    _fields = {
        'active': None,
        'code': None,
        'name': None,
        'resource_type': None,
        'time_efficiency': None,
        'calendar_id': {
              'name': 'calendar_id',
              'type': 'many2one',
              'relation': 'resource.calendar',
              'create': True # [CGM] Change to True if needed
        },
        'user_id': {
            'type': 'custom',
            'setter': 'set_user_id'
        },
    }

    def get_migration_data(self):
        self.source_model = self.source.ResourceResource
        self.dest_model = self.destination.ResourceResource

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

