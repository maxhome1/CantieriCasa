# -*- coding: utf-8 -*-
from .base import BaseCommand
from .settings import TAX_CODES, ACCOUNT_MAPPING

# ------------------------------------------------
# [CGM] One2Many fields
# - line_id
# ------------------------------------------------
# [CGM] Fields in source but not in destination
# - internal_sequence_number
# ------------------------------------------------
# [CGM] Fields in destination but not in source
# - __last_update
# - balance
# - create_date
# - create_uid
# - display_name
# - id
# - write_date
# - write_uid

class AccountMoveMigration(BaseCommand):

    _ignore_to_many_values = True

    _default_values = {
        'company_id': 1,
    }

    _fields = {
        'amount': None,
        'date': None,
        'name': None,
        'narration': None,
        'ref': None,
        'state': None,
        'to_check': None,
        'x_uuid': None,
        'journal_id': {
            'name': 'journal_id',
            'type': 'm2o',
            'relation': 'account.journal',
            'create': False, # [CGM] Change to True if needed
            'unique_field': 'code',
        },
        'line_id': {
            'type': 'custom',
            'setter': '_set_move_line',
        },
        'partner_id': {
            'name': 'partner_id',
            'type': 'm2o',
            'relation': 'res.partner',
            'create': False # [CGM] Change to True if needed
        },
        'period_id': {
            'name': 'period_id',
            'type': 'm2o',
            'relation': 'account.period',
            'create': False # [CGM] Change to True if needed
        },
    }

    def _set_move_line(self, old, new):
        move_lines = old.line_id
        if len(move_lines) == 0:
            return

        fields = [
            'amount_currency',
            # 'amount_residual', COMPUTED
            # 'amount_residual_currency', COMPUTED
            # 'balance', COMPUTED
            'blocked',
            'centralisation',
            'credit',
            'date',
            'date_created',
            'date_maturity',
            'debit',
            'name',
            'narration',
            'quantity',
            'ref',
            'state',
            'tax_amount',
            'x_uuid'
        ]

        new_lines = []
        for line in move_lines:

            new_line = {
                'company_id': 1,
                'currency_id': False
            }

            for field in fields:
                value = getattr(line, field)
                if value is not None:
                    new_line[field] = value

            # account_id
            if line.account_id:
                account_id = self.destination.AccountAccount.search(
                    [
                        '&',
                        ('code', '=', line.account_id.code),
                        ('type', '!=', 'view')
                    ],
                    context=self.default_context)
                if len(account_id) != 1:
                    # Maybe the name is incorrect, try with our
                    # custom mapping
                    # REALLY UGLY CODE AHEAD!
                    account = ACCOUNT_MAPPING.get(line.account_id.name)
                    if account is not None:
                        account_id = self.destination.AccountAccount.search(
                            [
                                # '&',
                                ('name', '=', account),
                                # ('type', '=', line.account_id.type)
                            ],
                            context=self.default_context)
                        if len(account_id) != 1:
                            if self.config['debug']:
                                print u"Account code not found '%s' not found " \
                                      u"even in the mapping, continue" % line.account_id.name
                            else:
                                msg = "Account code not found '%s' not found " \
                                      "even in the mapping" % line.account_id.name
                                raise KeyError(msg)
                        else:
                            new_line['account_id'] = account_id[0]
                    else:
                        if self.config['debug']:
                            if len(account_id) > 1:
                                new_line['account_id'] = account_id[0]
                            else:
                                print u"Account %s not yet imported, continue" % line.account_id.name
                        else:
                            raise KeyError("Account %s not found" % line.account_id.name)
                else:
                    new_line['account_id'] = account_id[0]

            # account_tax_id
            if line.account_tax_id:
                tax_id = self.destination.AccountTax.search(
                    [('name', '=', line.account_tax_id.name)],
                    context=self.default_context
                )
                if len(tax_id) != 1:
                    if self.config['debug']:
                        print "Tax not found (maybe not yet imported)"
                    else:
                        raise KeyError("Tax not found")
                else:
                    new_line['account_tax_id'] = tax_id[0]

            # analytic_account_id
            if line.analytic_account_id:
                analytic_account_id = self.destination.AccountAnalyticAccount.search(
                    [('name', '=', line.analytic_account_id.name)],
                    context=self.default_context)
                if len(analytic_account_id) != 1:
                    if self.config['debug']:
                        print "Analytic Account not found, continue"
                    else:
                        raise KeyError("Analytic Account '%s' not found" % line.analytic_account_id.name)
                else:
                    new_line['analytic_account_id'] = analytic_account_id[0]

            # invoice
            # Related from the invoice side

            # journal_id
            if line.journal_id:
                journal_id = self.destination.AccountJournal.search(
                    [('code', '=', line.journal_id.code)],
                    context=self.default_context)
                if len(journal_id) != 1:
                    if self.config['debug']:
                        print "Journal %s not yet imported, continue" % line.journal_id.code
                    else:
                        raise KeyError("Journal %s not yet imported, continue" % line.journal_id.code)
                else:
                    new_line['journal_id'] = journal_id[0]

            if line.partner_id:
                partner_id = self.destination.ResPartner.search(
                    [('name', '=', line.partner_id.name)],
                    context=self.default_context)
                if len(partner_id) != 1:
                    if self.config['debug']:
                        print "Partner not yet imported, continue"
                    else:
                        raise KeyError("Partner not found")
                else:
                    new_line['partner_id'] = partner_id[0]

            if line.period_id:
                period_id = self.destination.AccountPeriod.search(
                    [('name', '=', line.period_id.name)],
                    context=self.default_context)
                if len(period_id) != 1:
                    if self.config['debug']:
                        print "Period not yet imported, continue"
                    else:
                        raise KeyError("Period not found")
                else:
                    new_line['period_id'] = period_id[0]

            if line.product_id:
                product_id = self.destination.ProductProduct.search(
                    [
                        ('x_uuid', '=', line.product_id.x_uuid),
                    ],
                    context=self.default_context
                )
                if len(product_id) != 1:
                    if self.config['debug']:
                        print "Product not found (maybe not yet imported)"
                        continue
                    else:
                        raise KeyError("Product not found")
                new_line['product_id'] = product_id[0]

            if line.product_uom_id:
                # Trick: sometimes the uom of the product is not the same
                # of the movement: force it.
                uom_name = line.product_uom_id.name
                if line.product_id:
                    if line.product_id.uom_id.name != line.product_uom_id.name:
                        uom_name = line.product_id.uom_id.name
                uom_id = self.destination.ProductUom.search(
                    [('name', '=', uom_name)],
                    context=self.default_context
                )
                if len(uom_id) != 1:
                    if self.config['debug']:
                        print "Product UOM not found (maybe not yet imported)"
                        continue
                    else:
                        raise KeyError("Product UOM not found")
                new_line['product_uom_id'] = uom_id[0]

            # reconcile_id
            if line.reconcile_id:
                reconcile_id = self.destination.AccountMoveReconcile.search(
                    [('x_uuid', '=', line.reconcile_id.x_uuid)],
                    context=self.default_context
                )
                if len(reconcile_id) != 1:
                    if self.config['debug']:
                        print "Reconcile not found (maybe not yet imported)"
                        continue
                    else:
                        raise KeyError("Reconcile not found")
                new_line['reconcile_id'] = reconcile_id[0]

            # reconcile_partial_id
            if line.reconcile_partial_id:
                reconcile_partial_id = self.destination.AccountMoveReconcile.search(
                    [('x_uuid', '=', line.reconcile_partial_id.x_uuid)],
                    context=self.default_context
                )
                if len(reconcile_partial_id) != 1:
                    if self.config['debug']:
                        print "Reconcile partial not found (maybe not yet imported)"
                        continue
                    else:
                        raise KeyError("Reconcile partial not found")
                new_line['reconcile_partial_id'] = reconcile_partial_id[0]

            # statement_id
            if line.statement_id:
                statement_id = self.destination.AccountBankStatement.search(
                    [('name', '=', line.statement_id.name)],
                    context=self.default_context
                )
                if len(statement_id) != 1:
                    if self.config['debug']:
                        print "Statement not found (maybe not yet imported)"
                        continue
                    else:
                        raise KeyError("Statement not found")
                new_line['statement_id'] = statement_id[0]


            if line.tax_code_id:
                tax_code_id = self.destination.AccountTaxCode.search(
                    [
                        ('name', '=', line.tax_code_id.name),
                    ],
                    context=self.default_context)
                if len(tax_code_id) != 1:
                    # Maybe the name is incorrect, try with our
                    # custom mapping
                    # REALLY UGLY CODE AHEAD!
                    code = TAX_CODES.get(line.tax_code_id.name)
                    if code is not None:
                        tax_code_id = self.destination.AccountTaxCode.search(
                            [('code', '=', code)],
                            context=self.default_context)
                        if len(tax_code_id) != 1:
                            if self.config['debug']:
                                print "Tax code not found even in the mapping, continue"
                            else:
                                raise KeyError("Tax code '%s' not found even in the mapping" % line.tax_code_id.name)
                        else:
                            new_line['tax_code_id'] = tax_code_id[0]
                    else:
                        if self.config['debug']:
                            print "Tax code not found, continue"
                        else:
                            raise KeyError("Tax code '%s' not found even in the mapping" % line.tax_code_id.name)
                else:
                    new_line['tax_code_id'] = tax_code_id[0]

            new_lines.append((0, 0, new_line))

        new["line_id"] = new_lines

    def check_existent(self, record):
        """Search for duplicated records eg. for res.partner model.
        """
        return self.dest_model.search([
                ('x_uuid', '=', record['x_uuid']),
            ],
            context=self.default_context
        )

    def get_migration_data(self):
        self.source_model = self.source.AccountMove
        self.dest_model = self.destination.AccountMove

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

    def migrate(self):
        super(AccountMoveMigration, self).migrate()
