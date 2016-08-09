# -*- coding: utf-8 -*-
from .base import BaseCommand
 # 'bom_ids',
 # 'location_id',
 # 'packaging', > Always false
 # 'price_margin', > Not in odoo
 # 'procure_method', > Not in odoo
 # 'product_manager', > Only on 9 product, by hand
 # 'project_id', > Not in odoo (empty, btw)
 # 'property_account_expense', > Always false
 # 'property_account_income', > Always false
 # 'property_stock_account_input', > Always false
 # 'property_stock_account_output', > Always false
 # 'property_stock_inventory', > Always false
 # 'property_stock_procurement', > Always false
 # 'property_stock_production', > Always false
 # 'supply_method', > Not in odoo
 # 'variants', > Not in odoo



class ProductMigration(BaseCommand):
    """Product migration from Openerp 6 to Odoo 8
    """

    _fields = {
        "active": None,
        "categ_id": {
            "type": "custom",
            "setter": "_set_category",
        },
        "code": None,
        "cost_method": None,
        "default_code": None,
        "description": None,
        "description_purchase": None,
        "description_sale": None,
        "ean13": None,
        "incoming_qty": None,
        "list_price": None,
        "loc_case": None,
        "loc_rack": None,
        "loc_row": None,
        # "lst_price": None, https://bugs.launchpad.net/openobject-addons/+bug/677772
        "mes_type": None,
        "name": None,
        "name_template": None,
        "outgoing_qty": None,
        "partner_ref": None,
        "price": None,
        "price_extra": None,
        "pricelist_id": {
            "name": "pricelist_id",
            "type": "m2o",
            "relation": "product.pricelist",
            "create": False
        },
        "produce_delay": None,
        "purchase_ok": None,
        "qty_available": None,
        "rental": None,
        "sale_delay": None,
        "sale_ok": None,
        "seller_delay": None,
        "seller_id": {
            "name": "seller_id",
            "type": "m2o",
            "relation": "res.partner",
            "create": None
        },
        # Handled in productsupplierinfo
        # "seller_ids": {
        #     "type": "custom",
        #     "setter": "_set_seller_ids"
        # },
        "seller_qty": None,
        "standard_price": None,
        "state": None,
        "track_incoming": None,
        "track_outgoing": None,
        "track_production": None,
        "type": None,
        "uos_coeff": None,
        "valuation": None,
        "virtual_available": None,
        "volume": None,
        "warranty": None,
        "weight": None,
        "weight_net": None,
        "x_uuid": None,
        "company_id": {
            "name": "company_id",
            "type": "m2o",
            "relation": "res.company",
            "create": False
        },
        "taxes_id": {
            "type": "custom",
            "setter": "_set_taxes_id",
        },
        'supply_method': {
            'type': 'custom',
            'setter': '_set_route_ids',
        },
        "supplier_taxes_id": {
            "type": "custom",
            "setter": "_set_supplier_taxes_id",
        },
        "uom_id": {
            "name": "uom_id",
            "type": "m2o",
            "relation": "product.uom",
            "create": False
        },
        "uos_id": {
            "name": "uos_id",
            "type": "m2o",
            "relation": "product.uom",
            "create": False
        },
        "uom_po_id": {
            "name": "uom_po_id",
            "type": "m2o",
            "relation": "product.uom",
            "create": False
        },
    }

    _default_values = {
        "categ_id": 1
    }

    def __init__(self, *args, **kwargs):
        super(ProductMigration, self).__init__(*args, **kwargs)
        # A small optimization to cache to reused relations
        self._buy_route_ids = None
        self._produce_route_ids = None
        self._make_to_order_routs_ids = None

    def _set_route_ids(self, old, new):
        # In openerp6 supply_method and procure_method were simple text fields.
        # In odoo they are translated into a stock.location.route o2m field.
        # The procure_method 'make_to_stock' is the default and it is ignored.
        route_ids = []

        if old.supply_method == 'buy':
            if self._buy_route_ids is None:
                self._buy_route_ids = self.destination.StockLocationRoute.search(
                    [('name=Buy')],
                    context=self.default_context
                )
            route_ids.append((4, self._buy_route_ids[0]))
        elif old.supply_method == 'produce':
            if self._produce_route_ids is None:
                self._produce_route_ids = self.destination.StockLocationRoute.search(
                    [('name=Manufacture')],
                    context=self.default_context
                )
            route_ids.append((4, self._produce_route_ids[0]))

        if old.procure_method == 'make_to_order':
            if self._make_to_order_routs_ids is None:
                self._make_to_order_routs_ids = self.destination.StockLocationRoute.search(
                    [('name=Make To Order')],
                    context=self.default_context
                )
            route_ids.append((4, self._make_to_order_routs_ids[0]))

        new['route_ids'] = route_ids

    def _set_category(self, old, new):
        category = old.categ_id
        dest_model = self.destination.ProductCategory

        id_ = dest_model.search(
            [
                '&',
                ('name', '=', category.name),
                ('sequence', '=', category.sequence)
            ],
            context=self.default_context
        )
        if len(id_) == 1:
            new['categ_id'] = id_[0]
            return

        raise KeyError("Category not found")

    def _set_account_taxes_id(self, old, new, field):
        account_taxes_id = getattr(old, field, None)
        if account_taxes_id:
            taxes = []
            for tax in account_taxes_id:
                tax_id = self.destination.AccountTax.search(
                    [
                        ('name', '=', tax.name),
                    ],
                    context=self.default_context
                )
                if len(tax_id) != 1:
                    if self.config['debug']:
                        print "Tax {} not found (maybe not yet imported)".format(tax.name)
                        continue
                    else:
                        raise KeyError("Tax {} not found".format(tax.name))
                taxes.append((4, tax_id[0]))
            new[field] = taxes

    def _set_taxes_id(self, old, new):
        self._set_account_taxes_id(old, new, 'taxes_id')

    def _set_supplier_taxes_id(self, old, new):
        self._set_account_taxes_id(old, new, 'supplier_taxes_id')

    def check_existent(self, record):
        """Search for duplicated records eg. for res.partner model.
        """
        return self.dest_model.search([
                ('x_uuid', '=', record['x_uuid']),
            ],
            context=self.default_context
        )

    def get_migration_data(self):
        """Partner migration data:

        * source_model: Odoo 6 - product.product
        * dest_model: Odoo 8 - product.product
        * source_model_ids: all product ids
        * source_data: all product objects
        """
        self.source_model = self.source.ProductProduct
        self.dest_model = self.destination.ProductProduct

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
