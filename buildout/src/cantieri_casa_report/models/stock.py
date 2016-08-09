from openerp import fields
from openerp import models

class StockDddt(models.Model):

    _inherit = "stock.ddt"

    weight = fields.Float('Peso Lordo', default=0)
    weight_net = fields.Float('Peso Netto', default=0)
    delivery_address_id = fields.Many2one(
        'res.partner',
        string='Delivery Address',
        required=False
    )
