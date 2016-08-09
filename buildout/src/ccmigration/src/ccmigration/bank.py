# -*- coding: utf-8 -*-
from .base import BaseCommand


class BankMigration(BaseCommand):
    """Bank migration from Openerp 6 to Odoo 8
    """

    _fields = {
        'active': None,
        'bic': None,
        'city': None,
        'country': {
            "name": "country",
            "type": "m2o",
            "relation": "res.country",
            "create": False
        },
        'email': None,
        'fax': None,
        'name': None,
        'phone': None,
        'state': {
            "name": "state",
            "type": "m2o",
            "relation": "res.state",
            "create": False
        },
        'street': None,
        'street2': None,
        'zip': None
    }

    def get_migration_data(self):
        """Bank migration data:

        * source_model: Odoo 6 - res.bank
        * dest_model: Odoo 8 - res.bank
        * source_model_ids: all bank ids
        * source_data: partner objects
        """
        self.source_model = self.source.ResBank
        self.dest_model = self.destination.ResBank
        self.source_model_ids = self.source_model.search(
            [],
            order='id',
            context=self.default_context,
            limit=self.config['limit'],
            offset=self.config['offset']
        )

        if not self.source_model_ids:
            self.source_data = []
        else:
            self.source_data = self.source_model.browse(self.source_model_ids)
