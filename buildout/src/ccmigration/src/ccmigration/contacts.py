# -*- coding: utf-8 -*-
from .base import BaseCommand
from .address import AddressMixin


class ContactsMigration(BaseCommand, AddressMixin):
    """Contacts migration from Openerp 6 to Odoo 8
    """

    _fields = {
        "comment": None,
        "country_id": None,
        "email": None,
        "mobile": None,
        "function": None,
        "telephone": {"name": "phone"},
        "title": {
            "name": "title",
            "type": "m2o",
            "relation": "res.partner.title",
            "create": True
        },
        "website": None,
        "name": {
            "type": "custom",
            "setter": "get_name"
        },
        "street": {
            "type": "custom",
            "setter": "get_address"
        }
    }

    def get_migration_data(self):
        """Contacts migration data:

        * source_model: Odoo 6 - res.partner.contacts
        * dest_model: Odoo 8 - res.partner
        * source_model_ids: all  ids
        * source_data: all contacts objects
        """
        self.source_model = self.source.ResPartnerContact
        self.dest_model = self.destination.ResPartner

        self.source_model_ids = self.source_model.search(
            [
                '&',
                ('partner_id', '=', False),
                ('section_id', '=', False),
            ],
            order='id',
            limit=self.config['limit'],
            offset=self.config['offset'],
            context=self.default_context
        )

        if not self.source_model_ids:
            self.source_data = []
        else:
            self.source_data = self.source_model.browse(self.source_model_ids)

    def get_name(self, old, new):
        new['name'] = ''
        if old.name:
            new['name'] += old.name
        if old.first_name:
            if new['name']:
                new['name'] += ' '
            new['name'] += old.first_name

    def get_address(self, old, new):
        # skip contacts without job and address
        job = old.job_id
        if job is False:
            return

        omit_fields = self._fields.keys()

        job_fields = [
            "fax",
            "email",
            "fax",
            "function",
            "phone"
        ]

        def skip_old_fields(f_name):
            old_value = getattr(old, f_name)
            if old_value and not callable(old_value):
                return True
            return False

        for f_name in job_fields:
            # skip fields already populated
            if skip_old_fields(f_name):
                continue

            value = getattr(job, f_name)
            if not value:
                continue
            new[f_name] = getattr(job, f_name)

        address = job.address_id
        if address is False:
            return

        values = self.get_address_value(address)
        for f_name, value in values.items():
            # skip fields already populated
            if skip_old_fields(f_name):
                continue
            new[f_name] = value
