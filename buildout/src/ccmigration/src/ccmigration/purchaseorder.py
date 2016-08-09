# -*- coding: utf-8 -*-
from .base import BaseCommand


class PurchaseOrderMigration(BaseCommand):
    """PurchaseOrder migration from Openerp 6 to Odoo 8
    """

    _default_values = {
        'company_id': 1
    }

    _fields = {
        'amount_tax': None,
        'amount_total': None,
        'amount_untaxed': None,
        'date_approve': None,
        'date_order': None,
        'invoice_method': None,
        'invoiced': None,
        'invoiced_rate': None,
        'minimum_planned_date': None,
        'name': None,
        'notes': None,
        'origin': None,
        'partner_ref': None,
        'shipped': None,
        'shipped_rate': None,
        'state': None,
        'create_uid': {
            'type': 'custom',
            'setter': '_set_create_uid',
        },
        'dest_address_id': {
            'type': 'custom',
            'setter': '_set_dest_address_id'
        },
        # 'fiscal_position': None, # All empty
        # 'invoice_ids': None, # From invoices
        'location_id': {
            'name': 'location_id',
            'type': 'm2o',
            'relation': 'stock.location',
            'create': True
        },
        'order_line': {
            'type': 'custom',
            'setter': '_set_order_line'
        },
        # 'partner_address_id': nope
        'partner_id': {
            "name": "partner_id",
            "type": "m2o",
            "relation": "res.partner",
            "create": False
        },
        # 'picking_ids': None,# automagic
        'pricelist_id': {
            "name": "pricelist_id",
            "type": "m2o",
            "relation": 'product.pricelist',
            "create": False
        },
        'product_id': {
            "type": "custom",
            "setter": "_set_product"
        },
        'validator': {
            'type': 'custom',
            'setter': '_set_validator',
        },
        # 'warehouse_id': Not in odoo. But only from the main warehouse anyway
    }

    def _set_create_uid(self, old, new):
        self.set_user_id(old, new, field_name='create_uid')

    def _set_validator(self, old, new):
        self.set_user_id(old, new, field_name='validator')

    def _set_product(self, old, new):
        if not old.product_id:
            return

        product_id = self.destination.ProductProduct.browse(
            [
                ('x_uuid', '=', old.product_id.x_uuid),
            ],
            context=self.default_context
        )
        if len(product_id) != 1:
            if self.config['debug']:
                print "Product not found (maybe not yet imported)"
                return
            raise KeyError("Product not found")
        new['product_id'] = product_id[0]

    def _set_dest_address_id(self, old, new):
        return self.set_related_partner_id(old, new, 'dest_address_id')

    def _set_order_line(self, old, new):
        order_line = old.order_line
        if len(order_line) == 0:
            return

        fields = [
            # 'account_analytic_id', No analytics for now
            # 'company_id', by hand
            'date_order',
            'date_planned',
            # 'discount', not in odoo TODO Ask davide
            # 'invoice_lines',> readonly
            'invoiced',
            # 'move_dest_id', not in odoo
            # 'move_ids', automagic
            'name',
            'notes',
            # 'order_id',
            'price_subtotal',
            'price_unit',
            'product_qty',
            'state',
        ]

        new_lines = []
        for line in order_line:
            new_line = {}
            for field in fields:
                value = getattr(line, field)
                if value is not None:
                    new_line[field] = value

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

            if line.product_uom:
                product_uom = self.destination.ProductUom.search(
                    [
                        ('name', '=', line.product_uom.name),
                    ],
                    context=self.default_context
                )
                if len(product_uom) != 1:
                    if self.config['debug']:
                        print "Product UOM not found (maybe not yet imported)"
                        continue
                    else:
                        raise KeyError("Product UOM not found")
                new_line['product_uom'] = product_uom[0]

            if line.taxes_id:
                taxes = []
                for tax in line.taxes_id:
                    tax_id = self.destination.AccountTax.search(
                        [
                            ('name', '=', tax.name),
                        ],
                        context=self.default_context
                    )
                    if len(tax_id) != 1:
                        if self.config['debug']:
                            print "Tax not found (maybe not yet imported)"
                            continue
                        else:
                            raise KeyError("Tax not found")
                    taxes.append((4, tax_id[0]))
                new_line['taxes_id'] = taxes

            new_lines.append((0, 0, new_line))
        new["order_line"] = new_lines

    def get_migration_data(self):
        """Purchase order migration data:

        * source_model: Odoo 6 - Purchase.order
        * dest_model: Odoo 8 - Purchase.order
        * source_model_ids: all order ids
        * source_data: all uom objects
        """
        self.source_model = self.source.PurchaseOrder
        self.dest_model = self.destination.PurchaseOrder

        if self.config['debug']:
            self.source_model_ids = self.source_model.search(
                [],
                order='id',
                limit=self.config['limit'],
                offset=self.config['offset'],
                context=self.default_context
            )
        else:
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
