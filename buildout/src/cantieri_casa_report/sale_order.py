# -*- encoding: utf-8 -*-
import time
from openerp.report.report_sxw import rml_parse


class Parser(rml_parse):
    """ Sale Order Parser """

    def _amount_discount(self, sale_order):
        amount = 0.0
        for line in sale_order.order_line:
            discount = (line.discount / 100) * line.price_unit * line.product_uom_qty
            amount = amount + discount
        return amount

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'totalDiscount': self._amount_discount,
        })
