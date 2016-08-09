import argparse
import sys
# from . import ContactsMigration
from . import AccountAnalyticAccountMigration
from . import AccountBankStatementMigration
from . import AccountInvoiceMigration
from . import AccountJournalMigration
from . import AccountMoveMigration
from . import AccountMoveReconcileMigration
from . import AccountPaymentTermMigration
from . import AccountPeriodMigration
from . import AccountVoucherMigration
from . import BankMigration
from . import DummyDataMigration
from . import HrEmployeeMigration
from . import MrpBomMigration
from . import MrpRoutingMigration
from . import MrpWorkcenterMigration
from . import PartnerCategoryMigration
from . import PartnerMigration
from . import PartnerAddressMigration
from . import ProductCategoryMigration
from . import ProductMigration
from . import ProductPricelistMigration
from . import ProductPricelistItemMigration
from . import ProductSupplierinfoMigration
from . import PurchaseOrderMigration
from . import ResourceResourceMigration
from . import SaleOrderMigration
from . import StockProductionLotMigration
from . import StockPickingMigration
from . import UomMigration
from . import UsersMigration

from . import PopulateUUID
from . import FixContacts

class Application(object):
    """Command to perform Odoo migrations
    """
    commands = {
        'accountanalyticaccount': AccountAnalyticAccountMigration,
        'accountbankstatement': AccountBankStatementMigration,
        'accountinvoice': AccountInvoiceMigration,
        'accountjournal': AccountJournalMigration,
        'accountmove': AccountMoveMigration,
        'accountmovereconcile': AccountMoveReconcileMigration,
        'accountpaymentterm': AccountPaymentTermMigration,
        'accountperiod': AccountPeriodMigration,
        'accountvoucher': AccountVoucherMigration,
        'bank': BankMigration,
        'bom': MrpBomMigration,
        # base_contact is not installed in cantiericasa erp v6
        # 'contact': ContactsMigration,
        'dummydata': DummyDataMigration,
        'employee': HrEmployeeMigration,
        'partner': PartnerMigration,
        'partneraddress': PartnerAddressMigration,
        'partner_category': PartnerCategoryMigration,
        'product': ProductMigration,
        'productcategory': ProductCategoryMigration,
        'productpricelist': ProductPricelistMigration,
        'productpricelistitem': ProductPricelistItemMigration,
        'productsupplierinfo': ProductSupplierinfoMigration,
        'purchaseorder': PurchaseOrderMigration,
        'resource': ResourceResourceMigration,
        'routing': MrpRoutingMigration,
        'saleorder': SaleOrderMigration,
        'stockproductionlot': StockProductionLotMigration,
        'stockpicking': StockPickingMigration,
        'uom': UomMigration,
        'users': UsersMigration,
        'workcenter': MrpWorkcenterMigration,
        'populate_uuid': PopulateUUID,
        'fix_contacts': FixContacts
    }

    @classmethod
    def run(cls):
        parser = argparse.ArgumentParser(description=cls.__doc__)
        subparsers = parser.add_subparsers(
            title="Commands",
            description="Available migrations"
        )
        for k, target in cls.commands.items():
            subparser = subparsers.add_parser(k, help=target.__doc__)
            for o in target.options:
                if len(o) == 3:
                    subparser.add_argument(o[0], o[1], **o[2])
                else:
                    subparser.add_argument(o[0], **o[1])

            subparser.set_defaults(target=target)
        args = parser.parse_args()
        if hasattr(args, 'target'):
            sys.exit(args.target.main(args))
        else:
            parser.print_usage()
            sys.exit(-1)


def main():
    Application.run()

if __name__ == "__main__":
    main()
