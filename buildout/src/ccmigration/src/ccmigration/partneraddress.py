# -*- coding: utf-8 -*-
from .base import BaseCommand
from .address import AddressMixin


class PartnerAddressMigration(BaseCommand, AddressMixin):
    """Partner migration from Openerp 6 to Odoo 8
    """

    _fields = {
        "active": None,
        "birth_date": {"name": "birthdate"},
        "city": {
            "type": "custom",
            "setter": "_set_all_address_fields"
        },
        "company_id": {
            "name": "company_id",
            "type": "m2o",
            "relation": "res.company",
            "create": False
        },
        "name": None,
        "partner_id": {
            "type": "custom",
            "setter": "_set_parent_id"
        },
        "type": None,
    }

    def _set_all_address_fields(self, old, new):
        # it gets called by "city" but it's a shortcut for all fields
        new.update(self.get_address_value(old))

    def _set_parent_id(self, old, new):
        old_parent = old.partner_id
        if not old_parent:
            return

        parent = self.destination.ResPartner.search(
            [
                '&',
                ('name', '=', old_parent.name),
                ('vat', '=', old_parent.vat)
            ],
            context=self.default_context)

        if len(parent) != 1:
            if self.config['debug']:
                print "Error %s not found" % old_parent.name
            else:
                raise KeyError("Multiple partners or partner not found")
        else:
            new['parent_id'] = parent[0]

    def get_migration_data(self):
        """Partner migration data:

        * source_model: Odoo 6 - res.partner
        * dest_model: Odoo 8 - res.partner
        * source_model_ids: all partner ids not related to a user
                            and that are not company
        * source_data: partner objects
        """
        self.source_model = self.source.ResPartnerAddress
        self.dest_model = self.destination.ResPartner

        self.source_model_ids = self.source_model.search([
                ('type', '!=', 'default'),
                ('name', '!=', '')
            ],
            order='parent_id desc, id',
            context=self.default_context,
            limit=self.config['limit'],
            offset=self.config['offset'],
        )

        if not self.source_model_ids:
            self.source_data = []
        else:
            self.source_data = self.source_model.browse(self.source_model_ids)

