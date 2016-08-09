# -*- coding: utf-8 -*-
from .base import BaseCommand
from .settings import TAX_CODES

# ------------------------------------------------
# [CGM] One2Many fields
# - invoice_line
# - tax_line
# ------------------------------------------------
# [CGM] Fields in source but not in destination
# - abstract_line_ids
# - address_contact_id
# - address_invoice_id
# - vertical_comp
# - x_uuid
# ------------------------------------------------
# [CGM] Fields in destination but not in source
# - __last_update
# - commercial_partner_id
# - create_date
# - create_uid
# - ddt_id
# - display_name
# - id
# - message_follower_ids
# - message_ids
# - message_is_follower
# - message_last_post
# - message_summary
# - message_unread
# - parcels
# - paypal_url
# - section_id
# - sent
# - supplier_invoice_number
# - transportation_method_id
# - write_date
# - write_uid

class AccountInvoiceMigration(BaseCommand):

    _default_values = {
        # [CGM] Add any value shared by all instances of the model.
        #       Normally, fields like 'company_id' o 'currency_id' are good
        #       candidates.
        'company_id': 1,
        'currency_id': 1,
    }

    _fields = {
        # 'amount_tax': None,
        # 'amount_total': None,
        # 'amount_untaxed': None,
        # 'check_total': None,
        'comment': None,
        'date_due': None,
        'date_invoice': None,
        'internal_number': None,
        'move_name': None,
        'name': None,
        'number': None,
        'origin': None,
        'reconciled': None,
        'reference': None,
        'reference_type': None,
        # 'residual': None,
        'state': None,
        'type': None,
        'x_uuid': None,
        'account_id': {
              'unique_field': 'code',
              'name': 'account_id',
              'type': 'many2one',
              'relation': 'account.account',
              'create': False # [CGM] Change to True if needed
        },
        'carriage_condition_id': {
              'name': 'carriage_condition_id',
              'type': 'many2one',
              'relation': 'stock.picking.carriage_condition',
              'create': False # [CGM] Change to True if needed
        },
        # [CGM] The following field has no relations and
        #       can be commented out.
        # 'fiscal_position': {
        #       'name': 'fiscal_position',
        #       'type': 'many2one',
        #       'relation': 'account.fiscal.position',
        #       'create': False # [CGM] Change to True if needed
        # },
        'goods_description_id': {
              'name': 'goods_description_id',
              'type': 'many2one',
              'relation': 'stock.picking.goods_description',
              'create': False # [CGM] Change to True if needed
        },
        'journal_id': {
              'unique_field': 'code',
              'name': 'journal_id',
              'type': 'many2one',
              'relation': 'account.journal',
              'create': False # [CGM] Change to True if needed
        },
        'move_id': {
              'unique_field': 'x_uuid',
              'name': 'move_id',
              'type': 'many2one',
              'relation': 'account.move',
              'create': False # [CGM] Change to True if needed
        },
        'move_lines': {
              'unique_field': 'x_uuid',
              'name': 'move_lines',
              'type': 'many2many',
              'relation': 'account.move.line',
              'create': False # [CGM] Change to True if needed
        },
        # TODO
        # 'partner_bank_id': {
        #       'name': 'partner_bank_id',
        #       'type': 'many2one',
        #       'relation': 'res.partner.bank',
        #       'create': False # [CGM] Change to True if needed
        # },
        'partner_id': {
              'name': 'partner_id',
              'type': 'many2one',
              'relation': 'res.partner',
              'create': False # [CGM] Change to True if needed
        },
        'payment_ids': {
              'unique_field': 'x_uuid',
              'name': 'payment_ids',
              'type': 'many2many',
              'relation': 'account.move.line',
              'create': False # [CGM] Change to True if needed
        },
        'payment_term': {
              'name': 'payment_term',
              'type': 'many2one',
              'relation': 'account.payment.term',
              'create': False # [CGM] Change to True if needed
        },
        'period_id': {
              'name': 'period_id',
              'type': 'many2one',
              'relation': 'account.period',
              'create': False # [CGM] Change to True if needed
        },
        'supplier_invoice_number': {
            'type': 'custom',
            'setter': '_set_supplier_invoice_number'
        },
        'transportation_reason_id': {
              'name': 'transportation_reason_id',
              'type': 'many2one',
              'relation': 'stock.picking.transportation_reason',
              'create': False # [CGM] Change to True if needed
        },
        'user_id': {
              'type': 'custom',
              'setter': 'set_user_id'
        },
        'invoice_lines': {
            'type': 'custom',
            'setter': '_set_invoice_lines'
        },
        'tax_line': {
            'type': 'custom',
            'setter': '_set_tax_line'
        }
    }

    def _set_invoice_lines(self, old, new):
        invoice_lines = old.invoice_line
        if len(invoice_lines) == 0:
            return

        fields = [
            'discount',
            'name',
            'origin',
            'price_subtotal',
            'price_unit',
            'quantity',
            'sequence',
        ]

        new_lines = []
        for line in invoice_lines:
            new_line = {
                'company_id': 1
            }
            for field in fields:
                value = getattr(line, field)
                if value:
                    new_line[field] = value

            # account_analytic_id
            if line.account_analytic_id:
                account_analytic_id = self.destination.AccountAnalyticAccount.search(
                    [
                        ('name', '=', line.account_analytic_id.name),
                    ],
                    context=self.default_context
                )
                if len(account_analytic_id) != 1:
                    if self.config['debug']:
                        print "Analytic Account not yet imported, continue"
                    else:
                        raise KeyError("Analytic Account not found")
                else:
                    new_line['account_analytic_id'] = account_analytic_id[0]

            # account_id
            if line.account_id:
                account_id = self.destination.AccountAccount.search(
                    [
                        ('name', '=', line.account_id.name),
                    ],
                    context=self.default_context
                )
                if len(account_id) != 1:
                    if self.config['debug']:
                        print "Account not yet imported, continue"
                    else:
                        raise KeyError(
                            u"Account not found: %s [%s]" %
                            (line.account_id.name, line.account_id.code)
                        )
                else:
                    new_line['account_id'] = account_id[0]

            # invoice_line_tax_id
            tax_ids = []
            for tax in line.invoice_line_tax_id:
                id_ = self.destination.AccountTax.search(
                    [('name', '=', tax.name)],
                    context=self.default_context
                )
                if len(id_) != 1:
                    if self.config['debug']:
                        print "Tax not yet imported, continue"
                    else:
                        raise KeyError("Tax not found: {}".format(tax.name))
                else:
                    tax_ids.append(id_[0])
            new_line['invoice_line_tax_id'] = [(6, 0, tax_ids)]

            # partner_id
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
                        print "Product not yet imported, continue"
                    else:
                        raise KeyError("Product not found")
                else:
                    new_line['product_id'] = product_id[0]

            # uos_id
            if line.uos_id:
                uos_id = self.destination.ProductUom.search(
                    [('name', '=', line.uos_id.name)],
                    context=self.default_context
                )
                if len(uos_id) != 1:
                    if self.config['debug']:
                        print "UOM not yet imported, continue"
                    else:
                        raise KeyError("UOM not found")
                else:
                    new_line['uos_id'] = uos_id[0]

            new_lines.append((0, 0, new_line))

        new["invoice_line"] = new_lines

    def _set_tax_line(self, old, new):
        tax_line = old.tax_line
        if len(tax_line) == 0:
            return

        fields = [
            'amount',
            'base',
            'base_amount',
            'factor_base',
            'factor_tax',
            'manual',
            'name',
            'sequence',
            'tax_amount',
        ]

        new_lines = []
        for line in tax_line:
            new_line = {
                'company_id': 1
            }
            for field in fields:
                value = getattr(line, field)
                if value:
                    new_line[field] = value

            # account_id
            if line.account_id:
                account_id = self.destination.AccountAccount.search(
                    [
                        ('code', '=', line.account_id.code),
                    ],
                    context=self.default_context
                )
                if len(account_id) != 1:
                    if self.config['debug']:
                        print "Account not yet imported, continue"
                    else:
                        raise KeyError("Account not found")
                else:
                    new_line['account_id'] = account_id[0]

            for field in ('base_code_id', 'tax_code_id'):
                id_ = getattr(line, field, False)
                if id_:
                    tax_code_id = self.destination.AccountTaxCode.search(
                        [
                            ('name', '=', id_.name),
                        ],
                        context=self.default_context)


                    if len(tax_code_id) != 1:
                        # Maybe the name is incorrect, try with our
                        # custom mapping
                        # REALLY UGLY CODE AHEAD!
                        code = TAX_CODES.get(id_.name)
                        if code is not None:
                            tax_code_id = self.destination.AccountTaxCode.search(
                                [('code', '=', code)],
                                context=self.default_context)
                            if len(tax_code_id) != 1:
                                if self.config['debug']:
                                    print "Tax code not found even in the mapping, continue"
                                else:
                                    raise KeyError("Tax code '%s' not found even in the mapping" % line.tax_code_id.name)
                            else:
                                new_line[field] = tax_code_id[0]
                        else:
                            if self.config['debug']:
                                print "Tax code not found, continue"
                            else:
                                raise KeyError("Tax code '%s' not found even in the mapping" % line.tax_code_id.name)
                    else:
                        new_line[field] = tax_code_id[0]

            new_lines.append((0, 0, new_line))

        new["tax_line"] = new_lines

    def _set_supplier_invoice_number(self, old, new):
        if old.name:
            new['supplier_invoice_number'] = old.name

    def check_existent(self, record):
        """Search for duplicated records eg. for res.partner model.
        """
        return self.dest_model.search([
                ('x_uuid', '=', record['x_uuid']),
            ],
            context=self.default_context
        )

    def get_migration_data(self):
        self.source_model = self.source.AccountInvoice
        self.dest_model = self.destination.AccountInvoice

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

