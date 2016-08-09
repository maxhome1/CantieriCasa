# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _


class account_invoice(osv.osv):

    _inherit = 'account.invoice'

    def _get_address_invoice_id(self, cr, uid, ids, name, arg, context=None):
        res = {}
        res_partner_obj = self.pool['res.partner']
        for id_ in ids:
            partner_id = None
            invoice = self.browse(cr, uid, [id_])
            partner_id_addresses = res_partner_obj.address_get(cr, uid,
                [invoice.partner_id.id], ['invoice', 'contact'],
                context=context)
            address_types = ('invoice', 'default', 'contact')
            for address_type in address_types:
                if address_type in partner_id_addresses:
                    partner_id = partner_id_addresses[address_type]
                    break
            if partner_id is None:
                raise osv.except_osv(_('Error!'), _('Cannot find a suitable address.'))
            invoice_partner = res_partner_obj.browse(cr, uid, partner_id, context=context)
            res[id_] = invoice_partner.id
        return res

    _columns = {
        'address_invoice_id': fields.function(
            _get_address_invoice_id, method=True, type="many2one", obj="res.partner",
            string='Invoice Address', help=""),
        'sale_order_ids': fields.many2many(
            'sale.order', 'sale_order_invoice_rel', 'invoice_id',
            'order_id', 'Sale orders')
        }


account_invoice()
