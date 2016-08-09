# -*- encoding: utf-8 -*-

import time
from openerp.report.report_sxw import rml_parse


class Parser(rml_parse):
    """ Quotation Request Parser"""

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
        })
