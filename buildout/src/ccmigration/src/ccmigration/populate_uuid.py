# -*- coding: utf-8 -*-
import uuid

from .base import BaseCommand


class PopulateUUID(BaseCommand):
    def migrate(self):
        models = [
            'account.move',
            'account.move.line',
            'account.voucher',
            'account.voucher.line',
            'account.invoice',
            'account.move.reconcile',
            'product.product'
        ]
        for model_dotted_name in models:
            model = self._get_model(self.source, model_dotted_name)
            records = model.browse(
                [],
                limit=self.config['limit'],
                offset=self.config['offset']
            )
            total = len(records)
            for index, record in enumerate(records, 1):
                try:
                    skipped = True
                    if not record.x_uuid:
                        record.x_uuid = str(uuid.uuid1())
                        skipped = False
                except Exception:
                    print 'Error'
                finally:
                    if skipped:
                        tmpl = '[%s/%s] - skipped %s'
                    else:
                        tmpl = '[%s/%s] - %s'
                    print tmpl % (index, total, model_dotted_name)
