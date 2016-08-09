# -*- coding: utf-8 -*-
from .base import BaseCommand

# ------------------------------------------------
# [CGM] Fields in source but not in destination
# - bom_id
# - bom_lines
# - child_complete_ids
# - method
# - product_uos
# - product_uos_qty
# - revision_ids
# ------------------------------------------------
# [CGM] Fields in destination but not in source
# - __last_update
# - bom_line_ids
# - create_date
# - create_uid
# - display_name
# - id
# - message_follower_ids
# - message_ids
# - message_is_follower
# - message_last_post
# - message_summary
# - message_unread
# - product_tmpl_id
# - write_date
# - write_uid

class MrpBomMigration(BaseCommand):

    _default_values = {
        # [CGM] Add any value shared by all instances of the model.
        #       Normally, fields like 'company_id' o 'currency_id' are good
        #       candidates.
        'company_id': 1,
    }

    _fields = {
        'active': None,
        'code': None,
        'date_start': None,
        'date_stop': None,
        'name': None,
        'position': None,
        # TRICK
        # We use this field to store whether the bom was root or not
        'product_efficiency': {
            'type': 'custom',
            'setter': '_set_is_root'
        },
        'product_qty': None,
        # TRICK
        # We use this field to store the original id
        'product_rounding': {
            'type': 'custom',
            'setter': '_set_old_id'
        },
        'sequence': None,
        'type': None,
        # 'company_id': {
        #       'name': 'company_id',
        #       'type': 'many2one',
        #       'relation': 'res.company',
        #       'create': False # [CGM] Change to True if needed
        # },
        'product_id': {
              'type': 'custom',
              'setter': '_set_product',
        },
        'product_uom': {
              'name': 'product_uom',
              'type': 'many2one',
              'relation': 'product.uom',
              'create': False # [CGM] Change to True if needed
        },
        # [CGM] The following field has no relations and
        #       can be commented out.
        # 'property_ids': {
        #       'name': 'property_ids',
        #       'type': 'many2many',
        #       'relation': 'mrp.property',
        #       'create': False # [CGM] Change to True if needed
        # },
        'routing_id': {
              'name': 'routing_id',
              'type': 'many2one',
              'relation': 'mrp.routing',
              'create': False # [CGM] Change to True if needed
        },
    }

    def _set_product(self, old, new):
        if not old.product_id:
            return

        product_id = self.destination.ProductProduct.browse(
            [
                ('x_uuid', '=', old.product_id.x_uuid)
            ],
            context=self.default_context
        )
        if len(product_id) != 1:
            if self.config['debug']:
                print "Product not found (maybe not yet imported)"
            else:
                raise KeyError("Product not found")
        else:
            new['product_id'] = product_id[0]
            new['product_tmpl_id'] = product_id[0]

    def _set_is_root(self, old, new):
        if old.bom_id:
            new['product_efficiency'] = 2.0

    def _set_old_id(self, old, new):
        new['product_rounding'] = old.id

    def get_migration_data(self):
        self.source_model = self.source.MrpBom
        self.dest_model = self.destination.MrpBom

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

    def check_existent(self, record):
        # We want to migrate everything.
        # This means that the script can only run once.
        return False

    def migrate(self):

        def get_new_bom(old_id):
            new_bom = self.dest_model.browse(
                [('product_rounding', '=', old_id)]
            )
            if len(new_bom) == 1:
                return new_bom[0]

        def create_bom_line(old_bom, new_bom, parent_id):
            fields_from_new = [
                # 'child_line_ids', AUTOMAGIC
                'date_start',
                'date_stop',
                'product_efficiency',
                'product_qty',
                # 'product_rounding',
                'product_uom',
                # 'property_ids', EMPTY
                'routing_id',
                'sequence',
                'type',
            ]
            fields_from_old = [
                'product_uos',
                'product_uos_qty',
            ]
            line = {}
            for field in fields_from_new:
                value = getattr(new_bom, field)
                if value is not None:
                    line[field] = value

            for field in fields_from_old:
                value = getattr(old_bom, field)
                if value is not None:
                    line[field] = value

            line['bom_id'] = parent_id
            self._set_product(new_bom, line)
            del(line['product_tmpl_id'])
            return self.destination.MrpBomLine.create(line, context=self.default_context)


        # First, we migrate ALL the bom without taking into account parents,
        # children or whatsever, but we save the old bom id in the unused
        # product_rounding field.
        super(MrpBomMigration, self).migrate()

        # Next we retrieve the old children of each bom and we set the new ones
        # by using the aforementioned field
        n_total = len(self.source_data)
        for index, old_bom in enumerate(self.source_data, 1):
            print u"[{}/{}] Setting children of {}".format(
                index,
                n_total,
                self.dest_model._name
            )

            if len(old_bom.bom_lines) == 0:
                continue

            new_bom = get_new_bom(old_bom.id)
            new_bom_lines = []
            for old_line in old_bom.bom_lines:
                # new_line is actually a full bom, as it is imported from the
                # old system
                new_line= get_new_bom(old_line.id)
                if new_line is not None:
                    # new_bom_line is a mrp.bom.line instance, a type of object
                    # that does not exist in openerp
                    new_bom_line = create_bom_line(old_line, new_line, new_bom.id)
                    new_bom_lines.append(new_bom_line.id)
            new_bom.bom_line_ids = new_bom_lines

        # Restore the right value for product_rounding
        print "Restoring product_efficiency and product_rounding..."
        self.dest_model.browse([]).write({'product_efficiency': 1.0})
        self.destination.MrpBomLine.browse([]).write({'product_efficiency': 1.0})
        self.dest_model.browse([]).write({'product_rounding': 0.0})

        # Finally delete all leaves bom (that is: boms without components)
        print "Deleting leaves bom..."
        # self.dest_model.browse(['bom_line_ids=False']).unlink()

        # This should be useless, but we do it anyway: check that all the
        # referred products are 'Manufacture' and 'Make To Order'
        print "Checking the products are 'Manufacture' and 'Make To Order'..."
        products = self.dest_model.browse([]).read('product_id')

        manufacture_route_id = self.destination.StockLocationRoute.search(
            [('name=Manufacture')],
            context=self.default_context
        )[0]
        make_to_order_route_id = self.destination.StockLocationRoute.search(
            [('name=Make To Order')],
            context=self.default_context
        )[0]

        for product in products:
            route_ids = product.route_ids.id
            if not manufacture_route_id in route_ids:
                product.route_ids = [(4, manufacture_route_id)]
            if not make_to_order_route_id in route_ids:
                product.route_ids = [(4, make_to_order_route_id)]

# products = model('mrp.bom').browse([]).read('product_id')
# manufacture_route_id = model('stock.location.route').search([('name=Manufacture')])[0]
# make_to_order_route_id = model('stock.location.route').search([('name=Make To Order')])[0]
#
# for product in products:
#    route_ids = product.route_ids.id
#    if not manufacture_route_id in route_ids:
#      print "Missing manu"
#      product.route_ids = [(4, manufacture_route_id)]
#    if not make_to_order_route_id in route_ids:
#      print "Missing make"
#      product.route_ids = [(4, make_to_order_route_id)]
