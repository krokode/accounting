from decimal import Decimal
from django.test import TestCase
from django.utils import timezone

from apps.administration.models import Counterparty
from apps.warehouse.models import Product, Consignment, ConsignmentItem, StockMovement


class WarehouseTestCase(TestCase):
    def setUp(self):
        self.supplier = Counterparty.objects.create(name="Parts Global")
        self.product = Product.objects.create(
            sku="TST-SKU-1",
            name="Industrial Relay",
            quantity_on_hand=Decimal('5.00'),
            reorder_threshold=Decimal('10.00')
        )
        self.consignment = Consignment.objects.create(
            consignment_number="WB-9912",
            direction=Consignment.Direction.INWARD,
            counterparty=self.supplier,
            delivery_date=timezone.localdate()
        )
        ConsignmentItem.objects.create(
            consignment=self.consignment,
            product=self.product,
            quantity_expected=Decimal('20.00'),
            quantity_received=Decimal('20.00')
        )

    def test_low_stock_detection(self):
        self.assertTrue(self.product.is_low_stock)

    def test_consignment_confirmation_updates_stock(self):
        self.assertEqual(self.product.quantity_on_hand, Decimal('5.00'))

        self.consignment.confirm_and_update_stock()

        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity_on_hand, Decimal('25.00'))
        self.assertFalse(self.product.is_low_stock)

        # Check stock movement recorded
        movement = StockMovement.objects.filter(consignment=self.consignment).first()
        self.assertIsNotNone(movement)
        self.assertEqual(movement.quantity, Decimal('20.00'))
        self.assertEqual(movement.balance_after, Decimal('25.00'))
