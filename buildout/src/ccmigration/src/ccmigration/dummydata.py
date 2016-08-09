# -*- coding: utf-8 -*-
from .base import BaseCommand


class DummyDataMigration(BaseCommand):
    """Creates dummy data for debug and deployment env
    """

    _data = {
        # 'res.company': [
        #     {
        #         'name': "CANTIERI NAVALI CASA S.R.L.",
        #     }
        # ],
        # 'account.analytic.journal': [
        #     {
        #         'active': True,
        #         'code': 'SAL',
        #         'company_id': 1,
        #         'name': 'Sales',
        #         'type': 'sale',
        #     },
        #     {
        #         'active': True,
        #         'code': 'COM',
        #         'company_id': 1,
        #         'name': 'Commesse',
        #         'type': 'situation',
        #     },
        #     {
        #         'active': True,
        #         'code': 'TS',
        #         'company_id': 1,
        #         'name': 'Timesheet Journal',
        #         'type': 'general',
        #     }
        # ],
        'ir.sequence': [
            {
                'active': True,
                # 'code': 'account.journal',
                'company_id': 1,
                'name': '2010: Sale Journal',
                'number_increment': 1,
                'number_next': 7,
                'padding': 3,
                'prefix': '2010/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.journal',
                'company_id': 1,
                'name': '2011: Sale Journal',
                'number_increment': 1,
                'number_next': 18,
                'padding': 3,
                'prefix': '2011/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'stock.ddt',
                'company_id': 1,
                'name': '2012: DDT',
                'number_increment': 1,
                'number_next': 3,
                'padding': 3,
                'prefix': 'DDT/12/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.journal',
                'company_id': 1,
                'name': '2012: Sale Journal',
                'number_increment': 1,
                'number_next': 14,
                'padding': 3,
                'prefix': '2012/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'stock.ddt',
                'company_id': 1,
                'name': '2013: DDT',
                'number_increment': 1,
                'number_next': 1,
                'padding': 3,
                'prefix': 'DDT/13/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'purchase.order',
                'company_id': 1,
                'name': '2013: Purchase Order',
                'number_increment': 1,
                'number_next': 19,
                'padding': 4,
                'prefix': 'PO/13/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.journal',
                'company_id': 1,
                'name': '2013: Sale Journal',
                'number_increment': 1,
                'number_next': 12,
                'padding': 3,
                'prefix': '2013/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'sale.order',
                'company_id': 1,
                'name': '2013: Sale Order',
                'number_increment': 1,
                'number_next': 1,
                'padding': 3,
                'prefix': 'SO13',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'stock.ddt',
                'company_id': 1,
                'name': '2014: DDT',
                'number_increment': 1,
                'number_next': 1,
                'padding': 3,
                'prefix': 'DDT/14/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'purchase.order',
                'company_id': 1,
                'name': '2014: Purchase Order',
                'number_increment': 1,
                'number_next': 1,
                'padding': 4,
                'prefix': 'PO/14/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.journal',
                'company_id': 1,
                'name': '2014: Sale Journal',
                'number_increment': 1,
                'number_next': 21,
                'padding': 3,
                'prefix': '2014/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'sale.order',
                'company_id': 1,
                'name': '2014: Sale Order',
                'number_increment': 1,
                'number_next': 1,
                'padding': 3,
                'prefix': 'SO14',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'stock.ddt',
                'company_id': 1,
                'name': '2015: DDT',
                'number_increment': 1,
                'number_next': 1,
                'padding': 3,
                'prefix': 'DDT/15/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'purchase.order',
                'company_id': 1,
                'name': '2015: Purchase Order',
                'number_increment': 1,
                'number_next': 1,
                'padding': 4,
                'prefix': 'PO/15/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.journal',
                'company_id': 1,
                'name': '2015: Sale Journal',
                'number_increment': 1,
                'number_next': 1,
                'padding': 3,
                'prefix': '2015/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'sale.order',
                'company_id': 1,
                'name': '2015: Sale Order',
                'number_increment': 1,
                'number_next': 1,
                'padding': 3,
                'prefix': 'SO15',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.invoice.in_invoice',
                'company_id': 1,
                'name': 'Account Invoice In',
                'number_increment': 1,
                'number_next': 1,
                'padding': 3,
                'prefix': '%(year)s/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.invoice.out_invoice',
                'company_id': 1,
                'name': 'Account Invoice Out',
                'number_increment': 1,
                'number_next': 1,
                'padding': 3,
                'prefix': '%(year)s/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.journal',
                'company_id': 1,
                'name': 'Account Journal',
                'number_increment': 1,
                'number_next': 14,
                'padding': 0,
                'prefix': False,
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.invoice.in_refund',
                'company_id': 1,
                'name': 'Account Refund In',
                'number_increment': 1,
                'number_next': 1,
                'padding': 3,
                'prefix': '%(year)s/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.invoice.out_refund',
                'company_id': 1,
                'name': 'Account Refund Out',
                'number_increment': 1,
                'number_next': 1,
                'padding': 3,
                'prefix': '%(year)s/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.journal',
                'company_id': 1,
                'name': 'Bank Journal',
                'number_increment': 1,
                'number_next': 1,
                'padding': 3,
                'prefix': 'BNK/%(year)s/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.journal',
                'company_id': 1,
                'name': 'Bank Journal Cash',
                'number_increment': 1,
                'number_next': 396,
                'padding': 0,
                'prefix': False,
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.journal',
                'company_id': 1,
                'name': 'Bank Journal Current',
                'number_increment': 1,
                'number_next': 2623,
                'padding': 0,
                'prefix': False,
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.journal',
                'company_id': 1,
                'name': 'Bank Journal Deposit',
                'number_increment': 1,
                'number_next': 41,
                'padding': 0,
                'prefix': False,
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.journal',
                'company_id': 1,
                'name': 'Cash Journal',
                'number_increment': 1,
                'number_next': 1,
                'padding': 3,
                'prefix': 'CSH/%(year)s/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.journal',
                'company_id': 1,
                'name': 'Checks Journal',
                'number_increment': 1,
                'number_next': 1,
                'padding': 3,
                'prefix': 'CHK/%(year)s/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'cce',
                'company_id': 1,
                'name': 'Chiusura conto economico',
                'number_increment': 1,
                'number_next': 5,
                'padding': 4,
                'prefix': 'cce/%(year)s/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.journal',
                'company_id': 1,
                'name': 'Expenses Credit Notes Journal',
                'number_increment': 1,
                'number_next': 17,
                'padding': 3,
                'prefix': 'ECNJ/%(year)s/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.journal',
                'company_id': 1,
                'name': 'Internal Sequence Journal',
                'number_increment': 1,
                'number_next': 4726,
                'padding': 0,
                'prefix': False,
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'stock.picking.in',
                'company_id': 1,
                'name': 'Picking IN',
                'number_increment': 1,
                'number_next': 381,
                'padding': 5,
                'prefix': 'IN/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'stock.picking.out',
                'company_id': 1,
                'name': 'Picking OUT',
                'number_increment': 1,
                'number_next': 93,
                'padding': 5,
                'prefix': 'OUT/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'stock.lot.serial',
                'company_id': 1,
                'name': 'Production Lots',
                'number_increment': 1,
                'number_next': 15,
                'padding': 7,
                'prefix': False,
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.journal',
                'company_id': 1,
                'name': 'Purchase Journal',
                'number_increment': 1,
                'number_next': 970,
                'padding': 3,
                'prefix': 'EXJ/%(year)s/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.journal',
                'company_id': 1,
                # 'fiscal_ids': <RecordList 'account.sequence.fiscalyear,[1, 2, 3, 5, 9]'>,
                'name': 'Sale Journal',
                'number_increment': 1,
                'number_next': 51,
                'padding': 3,
                'prefix': '%(year)s/',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'sale.order',
                'company_id': 1,
                # 'fiscal_ids': <RecordList 'account.sequence.fiscalyear,[6, 12, 15]'>,
                'name': 'Sale Order',
                'number_increment': 1,
                'number_next': 8,
                'padding': 3,
                'prefix': 'SO%(y)s',
                'suffix': False
            },
            {
                'active': True,
                # 'code': 'account.journal',
                'company_id': 1,
                'name': 'Sales Credit Note Journal',
                'number_increment': 1,
                'number_next': 4,
                'padding': 3,
                'prefix': 'SCNJ/%(year)s/',
                'suffix': False
            }
        ]
        # 'account.tax': [
        #     'Esente IVA (credito)',
        #     'Esente IVA (debito)'
        # ]

    }

    def migrate(self):
        for m, v in self._data.items():
            model = self._get_model(self.destination, m)
            for i in v:
                ids = model.search(
                    [('name', '=', i['name'])],
                    context=self.default_context
                )
                if len(ids) == 0:
                    model.create(i)
