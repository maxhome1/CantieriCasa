# -*- encoding: utf-8 -*-
import time
from openerp.report.report_sxw import rml_parse


class Parser(rml_parse):
    """ Purchase Parser """

    def _get_codice_fornitore(self, line):
        supplier_id = line.partner_id
        if line.product_id:
            for supplier_info in line.product_id.seller_ids:
                if supplier_info.name == supplier_id:
                    return supplier_info.product_code
        return ''

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'get_codice_fornitore': self._get_codice_fornitore,
        })
