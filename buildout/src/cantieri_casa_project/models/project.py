# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Domsense s.r.l. (<http://www.domsense.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time

from openerp import _
from openerp import fields
from openerp import models
from openerp.osv import osv

class ProjectProject(models.Model):

    _inherit = "project.project"

    picking_type_id = fields.Many2one(
        'stock.picking.type',
        'Picking Type'
    )
    journal_id = fields.Many2one(
        'account.analytic.journal',
        'Analytic Journal'
    )


class ProjectTaskWorkMove(models.Model):

    _name = "project.task.work.move"
    _rec_name="product_id"

    product_id = fields.Many2one(
        'product.product',
        'Product'
    )
    product_qty = fields.Float('Quantity')
    task_work_move_id = fields.Many2one(
        'project.task.work',
        'Task Work Move'
    )


class project_task_work(models.Model):

    _inherit = 'project.task.work'

    name = fields.Text('Work summary')
    task_work_move_ids = fields.One2many(
        'project.task.work.move',
        'task_work_move_id',
        'Task Work Moves'
    )
    stock_picking_id = fields.Many2one(
        'stock.picking',
        'Stock Picking',
    )

    def action_consume_material(self, cr, uid, ids, context=None):
        """ Create stock.move and analytic.line for each product to comsume
        @return: True
        """
        for work in self.browse(cr, uid, ids, context=context):
            if not work.task_id.project_id:
                raise osv.except_osv(_('UserError'), _('There is no project defined'))
            if not work.task_id.project_id.picking_type_id:
                raise osv.except_osv(_('Bad Configuration !'),
                 _('No picking type defined for project "%s". \nFill in the administration tab of the project form.')% (work.task_id.project_id.name))
            if not work.task_id.project_id.journal_id:
                raise osv.except_osv(_('Bad Configuration !'),
                 _('No journal defined for project "%s". \nFill in the administration tab of the project form.')% (work.task_id.project_id.name))
            if work.stock_picking_id:
                raise osv.except_osv(_('UserError'), _('There is already a stock picking'))

            stock_picking_obj = self.pool.get('stock.picking')
            product_obj = self.pool.get('product.product')
            decimal_precision_obj = self.pool.get('decimal.precision')
            task_work_move_obj = self.pool.get('project.task.work.move')
            account_analytic_line_obj = self.pool.get('account.analytic.line')
            user = self.pool.get('res.users').browse(cr, uid, uid)
            partner = user.company_id.partner_id

            moves = []
            for task_work_move_id in work.task_work_move_ids:
                task_work_move = task_work_move_obj.browse(cr, uid, task_work_move_id.id)
                product = product_obj.browse(cr, uid, task_work_move.product_id.id)

                # Create a new account.analytic.line
                line = {}
                line['name'] = work.name
                line['date'] = time.strftime('%Y-%m-%d')
                prec = decimal_precision_obj.precision_get(cr, uid, 'Account')
                quantity = task_work_move.product_qty
                amount_unit = product.price_get('standard_price', context=context)[product.id]
                amount = amount_unit * quantity or 1.0
                # The amount has to be always negative
                line['amount']= -round(amount, prec)
                line['unit_amount'] = task_work_move.product_qty
                line['account_id'] = work.task_id.project_id.analytic_account_id.id
                line['product_uom_id'] = product.uom_id.id
                line['product_id'] = product.id

                ga = product.product_tmpl_id.property_account_expense.id
                if not ga:
                    ga = product.categ_id.property_account_expense_categ.id
                    if not ga:
                        raise osv.except_osv(_('Bad Configuration !'),
                                _('No product and product category property account defined on the related employee.\nFill in the timesheet tab of the employee form.'))

                line['general_account_id'] = ga
                line['journal_id']= work.task_id.project_id.journal_id.id
                account_analytic_line_obj.create(cr, uid, line)
                #Create a new stock.move
                move = {}
                move['product_id']= task_work_move.product_id.id
                move['product_uom_qty']= task_work_move.product_qty
                stock_warehouse_ids = self.pool.get('stock.warehouse').search(cr,uid,[('company_id','=',user.company_id.id)])

                if isinstance(stock_warehouse_ids, list) and  len(stock_warehouse_ids) > 0:
                    stock_warehouse = self.pool.get('stock.warehouse').browse(cr, uid, stock_warehouse_ids[0])
                    move['location_id']= work.task_id.project_id.picking_type_id.default_location_src_id.id 
                    move['location_dest_id'] = work.task_id.project_id.picking_type_id.default_location_dest_id.id 
                    uom = product.uom_id.id
                    move['product_uom']= uom
                    move['name']= product.name
                    moves.append([0,False,move])

        if len(moves) > 0:
            picking_data = {
                'partner_id': partner.id,
		'picking_type_id': work.task_id.project_id.picking_type_id.id,
                'move_lines': moves,
                'type': 'internal',
            }

            picking_id = stock_picking_obj.create(cr, uid, picking_data)
            self.write(cr, uid, ids, {'stock_picking_id': picking_id})

        return True
