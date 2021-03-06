# -*- coding: utf-8 -*-
from .accountanalyticaccount import AccountAnalyticAccountMigration
from .accountbankstatement import AccountBankStatementMigration
from .accountinvoice import AccountInvoiceMigration
from .accountjournal import AccountJournalMigration
from .accountmove import AccountMoveMigration
from .accountmovereconcile import AccountMoveReconcileMigration
from .accountpaymentterm import AccountPaymentTermMigration
from .accountperiod import AccountPeriodMigration
from .accountvoucher import AccountVoucherMigration
from .bank import BankMigration
from .contacts import ContactsMigration
from .dummydata import DummyDataMigration
from .hremployee import HrEmployeeMigration
from .mrpbom import MrpBomMigration
from .mrprouting import MrpRoutingMigration
from .mrpworkcenter import MrpWorkcenterMigration
from .partner import PartnerMigration
from .partneraddress import PartnerAddressMigration
from .partnercategory import PartnerCategoryMigration
from .product import ProductMigration
from .productcategory import ProductCategoryMigration
from .productpricelist import ProductPricelistMigration
from .productpricelistitem import ProductPricelistItemMigration
from .productsupplierinfo import ProductSupplierinfoMigration
from .purchaseorder import PurchaseOrderMigration
from .resourceresource import ResourceResourceMigration
from .saleorder import SaleOrderMigration
from .stockproductionlot import StockProductionLotMigration
from .stockpicking import StockPickingMigration
from .uom import UomMigration
from .users import UsersMigration

from .populate_uuid import PopulateUUID
from .fix_contacts import FixContacts
