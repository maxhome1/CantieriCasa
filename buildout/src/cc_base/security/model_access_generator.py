# -*- encoding: utf-8 -*-
# This script generates an ir.model.access.csv for Odoo/OpenERP
# based on some configuration defined in PERMISSIONS variable.
#
# How to configure:
# PERMISSION variable contains the description of model security permissions
# in this form:
# >>> {
# ...    'model.name': [
# ...        (
#                'group.name',
#                read permission,
#                write permission,
#                create permission,
#                unlink permission
#            )
# ...    ]
# ... }
#
# read, write ecc. permission can be defines by 1 (allow) or 0 (deny)
#
# USAGE:
# $ python model_access_generator.py
#
# enjoy!

# XXX: change me!
PERMISSIONS = {
    'my.model': [
        ('base.group_sale_salesman', 1, 1, 1, 0),
        ('base.group_sale_manager', 1, 1, 1, 0),
    ]
}

import os
import csv


class OdooModelAccessGenerator(object):

    _headers = [
        "id", "name", "model_id:id", "group_id:id",
        "perm_read", "perm_write", "perm_create", "perm_unlink"
    ]

    def __init__(self, permissions):
        self.permissions = permissions.copy()

    def brew_permissions(self, writer):
        for model, permissions in self.permissions.items():
            model_name = 'model_{}'.format(model.replace('.', '_'))
            for group, read, write, create, unlink in permissions:
                group_name = group.replace('.', '_')
                row = {
                    "id": "access_{}_{}".format(group_name, model_name),
                    "name": "Access {} {}".format(group, model_name),
                    "model_id:id": model_name,
                    "group_id:id": group,
                    "perm_read": read,
                    "perm_write": write,
                    "perm_create": create,
                    "perm_unlink": unlink
                }
                writer.writerow(row)

    def set_headers(self, writer):
        first_row = {}
        for i in self._headers:
            first_row[i] = i
        writer.writerow(first_row)

    def write(self):
        base_dir = os.path.dirname(__file__) or '.'
        _filename = '%s/ir.model.access.csv' % base_dir
        writer = csv.DictWriter(
            open(_filename, 'w'),
            fieldnames=self._headers,
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_NONNUMERIC
        )
        self.set_headers(writer)
        self.brew_permissions(writer)


if __name__ == "__main__":
    generator = OdooModelAccessGenerator(PERMISSIONS)
    generator.write()
