# -*- coding: utf-8 -*-
from .base import BaseCommand

# ------------------------------------------------
# [CGM] One2Many fields
# - move_lines
# ------------------------------------------------
# [CGM] Fields in source but not in destination
# - address_id
# - auto_picking
# - carrier_id
# - carrier_tracking_ref
# - ddt_date
# - ddt_number
# - number_of_packages
# - purchase_id
# - stock_journal_id
# - type
# - volume
# - weight
# - weight_net
# ------------------------------------------------
# [CGM] Fields in destination but not in source
# - __last_update
# - create_date
# - create_uid
# - ddt_id
# - ddt_type
# - display_name
# - group_id
# - id
# - message_follower_ids
# - message_ids
# - message_is_follower
# - message_last_post
# - message_summary
# - message_unread
# - owner_id
# - pack_operation_exist
# - pack_operation_ids
# - parcels
# - picking_type_code
# - picking_type_id
# - priority
# - product_id
# - quant_reserved_exist
# - reception_to_invoice
# - recompute_pack_op
# - transportation_method_id
# - write_date
# - write_uid

class StockPickingMigration(BaseCommand):

    _default_values = {
        # [CGM] Add any value shared by all instances of the model.
        #       Normally, fields like 'company_id' o 'currency_id' are good
        #       candidates.
        'company_id': 1
    }

    _fields = {
        'date': None,
        'date_done': None,
        'invoice_state': None,
        'max_date': None,
        'min_date': None,
        'move_type': None,
        'name': None,
        'note': {
            'type': 'custom',
            'setter': '_set_note'
        },
        'origin': None,
        'state': None,
        # We'll set it at the end of the process to be sure we have all
        # available picking imported
        # 'backorder_id': {
        #       'name': 'backorder_id',
        #       'type': 'many2one',
        #       'relation': 'stock.picking',
        #       'create': False # [CGM] Change to True if needed
        # },
        'carriage_condition_id': {
              'name': 'carriage_condition_id',
              'type': 'many2one',
              'relation': 'stock.picking.carriage_condition',
              'create': True # [CGM] Change to True if needed
        },
        'goods_description_id': {
              'name': 'goods_description_id',
              'type': 'many2one',
              'relation': 'stock.picking.goods_description',
              'create': True # [CGM] Change to True if needed
        },
        # [CGM] The following field has no relations and
        #       can be commented out.
        # 'location_dest_id': {
        #       'name': 'location_dest_id',
        #       'type': 'many2one',
        #       'relation': 'stock.location',
        #       'create': False # [CGM] Change to True if needed
        # },
        # [CGM] The following field has no relations and
        #       can be commented out.
        # 'location_id': {
        #       'name': 'location_id',
        #       'type': 'many2one',
        #       'relation': 'stock.location',
        #       'create': False # [CGM] Change to True if needed
        # },
        'partner_id': {
              'name': 'partner_id',
              'type': 'many2one',
              'relation': 'res.partner',
              'create': False # [CGM] Change to True if needed
        },
        'sale_id': {
            'type': 'custom',
            'setter': '_set_sale_id'
        },
        'transportation_reason_id': {
              'name': 'transportation_reason_id',
              'type': 'many2one',
              'relation': 'stock.picking.transportation_reason',
              'create': True # [CGM] Change to True if needed
        },
        'type': {
            'type': 'custom',
            'setter': '_set_type'
        },
        'move_lines': {
            'type': 'custom',
            'setter': '_set_move_lines'
        },
    }

    def _set_note(self, old, new):
        """We set the ddt_number and date in the note when present.
        """
        note = old.note
        if old.ddt_number:
            note = u'{} | {}'.format(note or '', old.ddt_number)
        if old.ddt_date:
            note = u'{} | {}'.format(note or '', old.ddt_date)
        new['note'] = note

    def _set_sale_id(self, old, new):
        # Try and pick a sale order. This is a best effort procedure, as
        # name and state field are not enough to achieve univocity.
        sale_id = old.sale_id
        if not sale_id:
            return

        dest_model = self.destination.SaleOrder
        id_ = dest_model.search(
            [
                '&',
                ('name', '=', sale_id.name),
                ('state', '=', sale_id.state)
            ],
            context=self.default_context
        )
        if len(id_) == 1:
            new['sale_id'] = id_[0]
            return

        if self.config['debug']:
            print "Order not yet imported, continue"
        else:
            raise KeyError("Order not found")

    def _set_type(self, old, new):

        # IMPORTANT We also set "parcels" (which is not present in the old
        # system) to the old picking id. We are going to use it to set the
        # backorder
        new['parcels'] = old.id

        picking_type = old.type
        if not picking_type:
            return

        # The internal name are changed
        dest_model = self.destination.StockPickingType
        mapping = {
            'in': 'incoming',
            'out': 'outgoing',
            'internal': 'internal'
        }
        picking_type_id = dest_model.search([
            ('code', '=', mapping.get(picking_type, 'internal'))
        ])
        new['picking_type_id'] = picking_type_id[0]

    def _set_move_lines(self, old, new):
        move_lines = old.move_lines
        if len(move_lines) == 0:
            return

        fields = [
            'create_date',
            'date',
            'date_expected',
            'name',
            'note',
            'origin',
            'price_unit',
            'priority',
            # 'product_qty',
            'product_uos_qty',
            'scrapped',
            'state',
            # 'backorder_id', > 133, maybe by hand later
            # 'move_dest_id', > TODO
            # 'picking_id', > API job
            # 'product_packaging', > Empty
            # 'production_id', > Only 32, by hand
            # 'purchase_line_id', > TODO
        ]

        new_lines = []
        for line in move_lines:
            new_line = {
                'company_id': 1
            }
            for field in fields:
                value = getattr(line, field)
                if value is not None:
                    new_line[field] = value

            new_line['product_uom_qty'] = getattr(line, 'product_qty')

            if line.partner_id:
                partner_id = self.destination.ResPartner.search(
                    [('name', '=', line.partner_id.name)],
                    context=self.default_context)
                if len(partner_id) != 1:
                    if self.config['debug']:
                        print "Partner not yet imported, continue"
                    else:
                        raise KeyError("Partner not found")
                else:
                    new_line['partner_id'] = partner_id[0]

            if line.product_id:
                product_id = self.destination.ProductProduct.search(
                    [
                        ('x_uuid', '=', line.product_id.x_uuid),
                    ],
                    context=self.default_context
                )
                if len(product_id) != 1:
                    if self.config['debug']:
                        print "Product not found (maybe not yet imported)"
                        continue
                    else:
                        raise KeyError("Product not found")
                new_line['product_id'] = product_id[0]

            uom_fields = ('product_uom', 'product_uos')
            for field in uom_fields:
                uom = getattr(line, field, False)
                if uom:
                    # Trick: sometimes the uom of the product is not the same
                    # of the movement: force it.
                    uom_name = uom.name
                    if line.product_id:
                        if line.product_id.uom_id.name != uom.name:
                            uom_name = line.product_id.uom_id.name
                    uom_id = self.destination.ProductUom.search(
                        [('name', '=', uom_name)],
                        context=self.default_context
                    )
                    if len(uom_id) != 1:
                        if self.config['debug']:
                            print "Product UOM not found (maybe not yet imported)"
                            continue
                        else:
                            raise KeyError("Product UOM not found")
                    new_line[field] = uom_id[0]

            location_fields = ('location_dest_id', 'location_id')
            for field in location_fields:
                location = getattr(line, field, False)
                if location:
                    location_id = self.destination.StockLocation.search(
                        [('name', '=', location.name)],
                        context=self.default_context
                    )
                    if len(location_id) != 1:
                        if self.config['debug']:
                            print "Location not found (maybe not yet imported)"
                            continue
                        else:
                            raise KeyError("Location not found")
                    new_line[field] = location_id[0]

            new_lines.append((0, 0, new_line))

        new["move_lines"] = new_lines

    def get_migration_data(self):
        self.source_model = self.source.StockPicking
        self.dest_model = self.destination.StockPicking

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

    def migrate(self):

        def get_new_picking(old_id):
            new_picking = self.dest_model.browse(
                [('parcels', '=', old_id)]
            )
            if len(new_picking) == 1:
                return new_picking[0]

        super(StockPickingMigration, self).migrate()
        print "Set backorders"

        n_total = len(self.source_data)
        for index, old_picking in enumerate(self.source_data, 1):
            print u"[{}/{}] Setting backorder - {}".format(
                index,
                n_total,
                old_picking.name
            )

            backorder = old_picking.backorder_id
            if not backorder:
                continue

            new_picking = get_new_picking(old_picking.id)
            new_backorder = get_new_picking(old_picking.backorder_id.id)

            new_picking.backorder_id = new_backorder
            # self.dest_model.browse([]).write({'parcels': 0})
