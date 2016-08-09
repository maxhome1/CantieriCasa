# -*- encoding: utf-8 -*-
import time
from report import report_sxw


class account_invoice(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(account_invoice, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
        })


class sale_order(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(sale_order, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
        })


class purchase_order(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(purchase_order, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
        })


class product_pricelist(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(product_pricelist, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
        })


class product_pricelist_eng(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(product_pricelist_eng, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
        })

report_sxw.report_sxw(
    'report.account_invoice',
    'account.invoice',
    'addons/cantieri_casa_report/templates/invoice.odt',
    parser=account_invoice)

report_sxw.report_sxw(
    'report.sale_order',
    'sale.order',
    'addons/cantieri_casa_report/templates/sale_order.odt',
    parser=sale_order)

report_sxw.report_sxw(
    'report.purchase_order',
    'purchase.order',
    'addons/cantieri_casa_report/templates/purchase_order.odt',
    parser=purchase_order)

report_sxw.report_sxw(
    'report.product_pricelist',
    'product.pricelist',
    'addons/cantieri_casa_report/templates/pricelist.odt',
    parser=product_pricelist)

report_sxw.report_sxw(
    'report.product_pricelist_eng',
    'product.pricelist',
    'addons/cantieri_casa_report/templates/pricelist_eng.odt',
    parser=product_pricelist_eng)
