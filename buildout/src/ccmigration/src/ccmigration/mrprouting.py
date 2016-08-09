# -*- coding: utf-8 -*-
from .base import BaseCommand

# ------------------------------------------------
# [CGM] One2Many fields
# - workcenter_lines
# ------------------------------------------------
# [CGM] Fields in destination but not in source
# - __last_update
# - create_date
# - create_uid
# - display_name
# - id
# - write_date
# - write_uid

class MrpRoutingMigration(BaseCommand):

    _default_values = {
        # [CGM] Add any value shared by all instances of the model.
        #       Normally, fields like 'company_id' o 'currency_id' are good
        #       candidates.
        'company_id': 1
    }

    _fields = {
        'active': None,
        'code': None,
        'name': None,
        'note': None,
        'location_id': {
              'name': 'location_id',
              'type': 'many2one',
              'relation': 'stock.location',
              'create': False # [CGM] Change to True if needed
        },
        'workcenter_lines': {
            'type': 'custom',
            'setter': '_set_workcenter_lines',
        }
    }

    def _set_workcenter_lines(self, old, new):
        workcenter_lines = old.workcenter_lines
        if len(workcenter_lines) == 0:
            return

        fields = [
            'cycle_nbr',
            'hour_nbr',
            'name',
            'note',
            'sequence',
        ]

        new_lines = []
        for line in workcenter_lines:
            new_line = {
                'company_id': 1
            }
            for field in fields:
                value = getattr(line, field)
                if value is not None:
                    new_line[field] = value

            if line.workcenter_id:
                workcenter_id = self.destination.MrpWorkcenter.search(
                    [
                        ('name', '=', line.workcenter_id.name),
                    ],
                    context=self.default_context
                )
                if len(workcenter_id) != 1:
                    if self.config['debug']:
                        print "Workcenter not found (maybe not yet imported)"
                        continue
                    else:
                        raise KeyError("Workcenter not found")
                new_line['workcenter_id'] = workcenter_id[0]

            new_lines.append((0, 0, new_line))

        new["workcenter_lines"] = new_lines

    def get_migration_data(self):
        self.source_model = self.source.MrpRouting
        self.dest_model = self.destination.MrpRouting

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

