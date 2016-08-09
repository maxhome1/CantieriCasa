# -*- encoding: utf-8 -*-
import time
from openerp.report.report_sxw import rml_parse


class Parser(rml_parse):
    """ Price List Parser """

    def _getCategories(self, pricelist_version):
        categories = []
        categories_dict = {}
        for item in pricelist_version.items_id:
            if item.product_id:
                categ = item.product_id.categ_id
                if categ not in categories:
                    categories_dict[categ.name] = categ
        for key in sorted(categories_dict.iterkeys()):
            categories.append(categories_dict[key])
        for categoria in categories:
            if categoria.name.lower().startswith('casa'):
                casa_categ = categoria
                categories.remove(categoria)
                categories.insert(0, casa_categ)
        return categories

    def _getProducts(self, pricelist_version, categ_id):
        products = []
        for item in pricelist_version.items_id:
            if item.product_id:
                if item.product_id.categ_id.id == categ_id:
                    products.append(item.product_id)
        return products

    def _set_lang(self, lang):
        self.setLang(lang)
        return True

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'getCategories': self._getCategories,
            'getProducts': self._getProducts,
            'set_lang': self._set_lang,
        })
