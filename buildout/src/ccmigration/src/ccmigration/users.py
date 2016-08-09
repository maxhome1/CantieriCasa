# -*- coding: utf-8 -*-
from .base import BaseCommand
from .address import AddressMixin


class UsersMigration(BaseCommand, AddressMixin):
    """User migration from Openerp 6 to Odoo 8
    """

    _default_values = {
        'company_id': 1
    }

    _fields = {
        'active': None,
        'date': None,
        'email': None,
        'login': None,
        'name': None,
        'new_password': None,
        'password': None,
        'signature': None,
        # 'action_id' > Empty
        'address_id': {
            "type": "custom",
            "setter": "get_address"
        },
        # 'availability' > Does not exist
        # 'company_id' > Default 1
        # 'company_ids'
        # 'context_department_id' > Does not exist
        # 'context_lang' > Does not exist
        # 'context_project_id' > Does not exist
        # 'context_section_id' > Does not exist
        # 'context_tz' > Does not exist
        # 'groups_id' > TODO By hand
        # 'menu_id' > Does not exist
        # 'menu_tips' > Does not exist
        # 'user_email' > Does not exist
     }

    def get_address(self, old, new):
        if not old.address_id:
            return

        new.update(self.get_address_value(old.address_id))

    def get_migration_data(self):
        """Contacts migration data:

        * source_model: Odoo 6 - res.users
        * dest_model: Odoo 8 - res.users
        * source_model_ids: all  ids
        * source_data: all contacts objects
        """
        self.source_model = self.source.ResUsers
        self.dest_model = self.destination.ResUsers

        # All users but the admin
        self.source_model_ids = self.source_model.search(
            [('id!=1'), '|', ('active=False'), ('active=True')],
            order='id',
            limit=self.config['limit'],
            offset=self.config['offset'],
            context=self.default_context
        )

        if not self.source_model_ids:
            self.source_data = []
        else:
            self.source_data = self.source_model.browse(self.source_model_ids)
