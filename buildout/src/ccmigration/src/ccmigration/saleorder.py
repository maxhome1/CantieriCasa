# -*- coding: utf-8 -*-
from .base import BaseCommand

# ------------------------------------------------
# [CGM] One2Many fields
# - order_line
# - picking_ids
# ------------------------------------------------
# [CGM] Fields in source but not in destination
# - abstract_line_ids
# - carrier_id
# - commitment_date
# - effective_date
# - invoice_quantity
# - partner_order_id
# - picked_rate
# - requested_date
# - shop_id
# - validity
# ------------------------------------------------
# [CGM] Fields in destination but not in source
# - __last_update
# - campaign_id
# - carriage_condition_id
# - categ_ids
# - create_ddt
# - create_uid
# - currency_id
# - ddt_ids
# - display_name
# - goods_description_id
# - invoice_exists
# - medium_id
# - message_follower_ids
# - message_ids
# - message_is_follower
# - message_last_post
# - message_summary
# - message_unread
# - parcels
# - paypal_url
# - procurement_group_id
# - product_id
# - source_id
# - transportation_method_id
# - transportation_reason_id
# - warehouse_id
# - write_date
# - write_uid

class SaleOrderMigration(BaseCommand):

    _ignore_to_many_values = 1

    _default_values = {
        # [CGM] Add any value shared by all instances of the model.
        #       Normally, fields like 'company_id' o 'currency_id' are good
        #       candidates.
        'company_id': 1,
        'user_id': 1,
    }

    _fields = {
        'amount_tax': None,
        'amount_total': None,
        'amount_untaxed': None,
        'client_order_ref': None,
        'create_date': None,
        'date_confirm': None,
        'date_order': None,
        'invoiced': None,
        'invoiced_rate': None,
        'name': None,
        'note': None,
        'origin': None,
        'picking_policy': None,
        'shipped': None,
        'state': None,
        # [CGM] The following field has no relations and
        #       can be commented out.
        # 'fiscal_position': {
        #       'name': 'fiscal_position',
        #       'type': 'many2one',
        #       'relation': 'account.fiscal.position',
        #       'create': False # [CGM] Change to True if needed
        # },
        # [CGM] The following field has no relations and
        #       can be commented out.
        # 'incoterm': {
        #       'name': 'incoterm',
        #       'type': 'many2one',
        #       'relation': 'stock.incoterms',
        #       'create': False # [CGM] Change to True if needed
        # },
        # XXX These come from the invoices migration
        # 'invoice_ids': {
        #       'name': 'invoice_ids',
        #       'type': 'many2many',
        #       'relation': 'account.invoice',
        #       'create': False # [CGM] Change to True if needed
        # },
        'order_line': {
            'type': 'custom',
            'setter': '_set_order_line',
        },
        'order_policy': {
            'type': 'custom',
            'setter': '_set_order_policy',
        },
        'partner_id': {
              'name': 'partner_id',
              'type': 'many2one',
              'relation': 'res.partner',
              'create': False # [CGM] Change to True if needed
        },
        'payment_term': {
              'name': 'payment_term',
              'type': 'many2one',
              'relation': 'account.payment.term',
              'create': False # [CGM] Change to True if needed
        },
        'pricelist_id': {
              'name': 'pricelist_id',
              'type': 'many2one',
              'relation': 'product.pricelist',
              'create': False # [CGM] Change to True if needed
        },
        # [CGM] The following field has no relations and
        #       can be commented out.
        # 'project_id': {
        #       'name': 'project_id',
        #       'type': 'many2one',
        #       'relation': 'account.analytic.account',
        #       'create': False # [CGM] Change to True if needed
        # },
        # XXX: CRM > NOT NOW
        # 'section_id': {
        #       'name': 'section_id',
        #       'type': 'many2one',
        #       'relation': 'crm.case.section',
        #       'create': False # [CGM] Change to True if needed
        # },
        'user_id': {
            'type': 'custom',
            'setter': 'set_user_id'
        },
    }

    def _set_order_line(self, old, new):
        order_line = old.order_line
        if len(order_line) == 0:
            return

        fields = [
            'delay',
            'discount',
            'invoiced',
            'name',
            'number_packages',
            'price_subtotal',
            'price_unit',
            'product_uom_qty',
            'product_uos_qty',
            'sequence',
            'state',
            'th_weight',
        ]

        new_lines = []
        for line in order_line:
            new_line = {
                'company_id': 1,
            }
            for field in fields:
                value = getattr(line, field)
                if value is not None:
                    new_line[field] = value

            # product_id
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

            # tax_id
            if line.tax_id:
                taxes = []
                for tax in line.tax_id:
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

                new_line['tax_id'] = taxes

            # salesman_id
            if line.salesman_id:
                salesman_id = self.destination.ResUsers.search(
                    [
                        ('name', '=', line.salesman_id.name),
                        '|', ('active=False'), ('active=True'),
                    ],
                    context=self.default_context
                )
                if len(salesman_id) != 1:
                    if self.config['debug']:
                        print "User not found (maybe not yet imported)"
                        continue
                    else:
                        raise KeyError("User not found")
                new_line['salesman_id'] = salesman_id[0]

            uom_fields = ('product_uom', 'product_uos')
            for uom_field in uom_fields:
                uom = getattr(line, uom_field)
                if not uom:
                    continue
                uom_field_value = self.destination.ProductUom.search(
                    [('name', '=', uom.name)],
                    context=self.default_context
                )
                if len(uom_field_value) != 1:
                    if self.config['debug']:
                        print "Product UO[M/S] not found (maybe not yet imported)"
                        continue
                    else:
                        raise KeyError("Product UO[M/S] not found")
                else:
                    new_line[uom_field] = uom_field_value[0]

            new_lines.append((0, 0, new_line))

        new["order_line"] = new_lines

    def _set_order_policy(self, old, new):
        old_policy = old.order_policy
        if old_policy == 'postpaid':
            old_policy = 'manual'
        new['order_policy'] = old_policy

    def check_existent(self, record):
        """Search for duplicated records eg. for res.partner model.
        """
        return self.dest_model.search([
                '&',
                ('name', '=', record['name']),
                ('state', '=', record['state'])
            ],
            context=self.default_context
        )

    def get_migration_data(self):
        self.source_model = self.source.SaleOrder
        self.dest_model = self.destination.SaleOrder

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
            ['state != "cancel"'],
            order='id',
            limit=self.config['limit'],
            offset=self.config['offset'],
            context=self.default_context
        )
        if self.source_model_ids:
            self.source_data = self.source_model.browse(self.source_model_ids)

