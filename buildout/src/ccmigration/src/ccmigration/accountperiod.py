# -*- coding: utf-8 -*-
from .base import BaseCommand


class AccountPeriodMigration(BaseCommand):
    """AccountPeriodMigration migration from Openerp 6 to Odoo 8
    """

    _default_values = {
        'state': 'draft'
    }

    _fields = {
        'code': None,
        'company_id': None,
        'date_start': None,
        'date_stop': None,
        'name': None,
        'special': None,
        'state': None,
        'fiscalyear_id': {
            'type': 'custom',
            'setter': '_set_fiscalyear_id'
        }
    }

    def _set_fiscalyear_id(self, old, new):
        if not old.fiscalyear_id:
            return

        fiscalyear_id = self.destination.AccountFiscalyear.browse([
            ('name', '=', old.fiscalyear_id.name),
        ])

        if len(fiscalyear_id) == 1:
            new['fiscalyear_id'] = fiscalyear_id[0].id
        else:
            _new_fiscalyear = {
                'state': 'draft'
            }
            fields = [
                'code',
                'date_start',
                'date_stop',
                'name',
                # 'state' > Keep it open to trigger the invoice workflow later
            ]
            for field in fields:
                value = getattr(old.fiscalyear_id, field)
                if value is not None:
                    _new_fiscalyear[field] = value
            new_id = self.destination.AccountFiscalyear.create(_new_fiscalyear)
            new['fiscalyear_id'] = new_id.id

    def get_migration_data(self):
        """AccountPeriod migration data:

        * source_model: Odoo 6 - account.period
        * dest_model: Odoo 8 - account.period
        * source_model_ids: all account.period ids
        * source_data: all account.period objects
        """
        self.source_model = self.source.AccountPeriod
        self.dest_model = self.destination.AccountPeriod

        self.source_model_ids = self.source_model.search(
            [],
            order='id',
            limit=self.config['limit'],
            offset=self.config['offset'],
            context=self.default_context
        )
        if not self.source_model_ids:
            self.source_data = []
        else:
            self.source_data = self.source_model.browse(self.source_model_ids)
