# -*- coding: utf-8 -*-
from .base import BaseCommand


class AccountPaymentTermMigration(BaseCommand):
    """AccountPaymentTerm migration from Openerp 6 to Odoo 8
    """

    _fields = {
        "active": None,
        "name": None,
        "note": None,
        "line_ids": {
            "type": "custom",
            "setter": "_get_lines"
        }
    }

    def _get_lines(self, old, new):
        line_ids = old.line_ids
        if len(line_ids) == 0:
            return

        fields = [
            "days",
            "days2",
            "name",
            "sequence",
            "value",
            "value_amount"
        ]

        new_lines = []
        for line in line_ids:
            new_line = {}
            for field in fields:
                value = getattr(line, field)
                if value is not None:
                    new_line[field] = value
            new_lines.append((0, 0, new_line))

        new["line_ids"] = new_lines

    def get_migration_data(self):
        """AccountPaymentTerm migration data:

        * source_model: Odoo 6 - account.payment.term
        * dest_model: Odoo 8 - account.payment.term
        * source_model_ids: all account.payment.term ids
        * source_data: all account.payment.term objects
        """
        self.source_model = self.source.AccountPaymentTerm
        self.dest_model = self.destination.AccountPaymentTerm

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
