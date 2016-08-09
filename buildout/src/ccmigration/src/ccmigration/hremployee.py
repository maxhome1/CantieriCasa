# -*- coding: utf-8 -*-
from .base import BaseCommand

# ------------------------------------------------
# [CGM] One2Many fields
# - child_ids
# ------------------------------------------------
# [CGM] Fields in source but not in destination
# - journal_id
# - partner_id
# - photo
# - product_id
# - state
# ------------------------------------------------
# [CGM] Fields in destination but not in source
# - __last_update
# - city
# - color
# - create_date
# - create_uid
# - display_name
# - id
# - image
# - image_medium
# - image_small
# - last_login
# - login
# - message_follower_ids
# - message_ids
# - message_is_follower
# - message_last_post
# - message_summary
# - message_unread
# - name_related
# - otherid
# - write_date
# - write_uid

class HrEmployeeMigration(BaseCommand):

    _default_values = {
        # [CGM] Add any value shared by all instances of the model.
        #       Normally, fields like 'company_id' o 'currency_id' are good
        #       candidates.
        'company_id': 1,
    }

    _fields = {
        'active': None,
        'birthday': None,
        'code': None,
        'gender': None,
        'identification_id': None,
        'mobile_phone': None,
        'name': None,
        'notes': None,
        'passport_id': None,
        'resource_type': None,
        'sinid': None,
        'ssnid': None,
        'time_efficiency': None,
        'work_email': None,
        'work_location': None,
        'work_phone': None,
        # [CGM] The following field has no relations and
        #       can be commented out.
        # 'bank_account_id': {
        #       'name': 'bank_account_id',
        #       'type': 'many2one',
        #       'relation': 'res.partner.bank',
        #       'create': False # [CGM] Change to True if needed
        # },
        # [CGM] The following field has no relations and
        #       can be commented out.
        # 'calendar_id': {
        #       'name': 'calendar_id',
        #       'type': 'many2one',
        #       'relation': 'resource.calendar',
        #       'create': False # [CGM] Change to True if needed
        # },
        # [CGM] The following field has no relations and
        #       can be commented out.
        # 'category_ids': {
        #       'name': 'category_ids',
        #       'type': 'many2many',
        #       'relation': 'hr.employee.category',
        #       'create': False # [CGM] Change to True if needed
        # },
        # [CGM] The following field has no relations and
        #       can be commented out.
        # 'coach_id': {
        #       'name': 'coach_id',
        #       'type': 'many2one',
        #       'relation': 'hr.employee',
        #       'create': False # [CGM] Change to True if needed
        # },
        'country_id': {
              'name': 'country_id',
              'type': 'many2one',
              'relation': 'res.country',
              'create': False # [CGM] Change to True if needed
        },
        'department_id': {
              'name': 'department_id',
              'type': 'many2one',
              'relation': 'hr.department',
              'create': True # [CGM] Change to True if needed
        },
        # [CGM] The following field has no relations and
        #       can be commented out.
        # 'job_id': {
        #       'name': 'job_id',
        #       'type': 'many2one',
        #       'relation': 'hr.job',
        #       'create': False # [CGM] Change to True if needed
        # },
        # 'parent_id': {
        #       'name': 'parent_id',
        #       'type': 'many2one',
        #       'relation': 'hr.employee',
        #       'create': False # [CGM] Change to True if needed
        # },
        'resource_id': {
              'name': 'resource_id',
              'type': 'many2one',
              'relation': 'resource.resource',
              'create': False # [CGM] Change to True if needed
        },
        'user_id': {
            'type': 'custom',
            'setter': 'set_user_id'
        },
    }

    def migrate(self, *args, **kwargs):
        super(HrEmployeeMigration, self).migrate(*args, **kwargs)
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

    def get_migration_data(self):
        self.source_model = self.source.HrEmployee
        self.dest_model = self.destination.HrEmployee

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

