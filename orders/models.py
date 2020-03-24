import uuid

from django.db import models

# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField


class OrderManager(models.Manager):

    def get_last_order(self, ration_card):
        return super.get_queryset().filter(ration_card_no=ration_card).latest()


class Order(models.Model):
    pk = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name_applied = models.CharField(max_length=100, null=False, blank=False)
    time = models.DateTimeField(auto_now_add=True)
    address = models.TextField(null=False, blank=False)
    shop = models.ForeignKey('orders.Shop', on_delete=models.SET_NULL, related_name='shop_orders')
    ration_card_no = models.CharField(max_length=10, null=False, blank=True)
    phone = PhoneNumberField(null=False, blank=False)
    is_delivered = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    volunteer = models.ForeignKey('', on_delete=models.PROTECT, related_name='orders')
    bill = models.ImageField()
    objects = OrderManager()

    def cancel(self):
        self.is_cancelled = True
        self.save()

    def delivered(self):
        self.is_delivered = True
        self.save()

    def check_valid_by_date(self):
        last_order = self.objects.get_last_order(self.ration_card_no)
        # check difference of date is 3

    # for easy sectioning in order detail
    def get_fruits_and_vegetables_order_items(self):
        return self.items.filter(item__category=2)

    def get_grocery_order_items(self):
        return self.items.filter(item__category=0)

    def get_medicines_order_items(self):
        return self.items.filter(item__category=1)

    def get_ration_order_items(self):
        return self.items.filter(item__category=13)

    class Meta:
        ordering = ("-time",)


class ItemManager(models.Manager):

    def get_grocery_items(self):
        return super().get_queryset().filter(category=0)

    def get_medicine_items(self):
        return super().get_queryset().filter(category=1)

    def get_fruits_and_vegetables_items(self):
        return super().get_queryset().filter(category=2)

    def get_ration_items(self):
        return super().get_queryset().filter(category=3)


class Item(models.Model):
    GROCERY = 0
    MEDICINES = 1
    FRUITS_AND_VEGETABLE = 2
    RATION = 3

    KG = 0
    PACKET = 1

    CATEGORY = (
        (GROCERY, 'Grocery'),
        (MEDICINES, 'Medicines'),
        (FRUITS_AND_VEGETABLE, 'Fruits and Vegetable'),
        (RATION, 'Ration')
    )
    QUANTITY_TYPE = (
        (KG, 'KG'),
        (PACKET, 'Packet'),
    )
    name = models.CharField(max_length=50, null=False, blank=False)
    category = models.IntegerField(choices=CATEGORY, blank=False)
    quantity_type = models.IntegerField(choices=QUANTITY_TYPE, blank=False)
    max_quantity = models.FloatField(blank=False, null=False)
    objects = ItemManager()


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='order_items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    quantity = models.FloatField()
    brand = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return '{} - {} {}'.format(self.item.name, self.quantity, self.item.quantity_type)

    def check_max_quantity(self):
        return self.quantity > self.item.max_quantity


class Shop(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=200, blank=False)
    owner = models.CharField(max_length=100, blank=False)
    phone = PhoneNumberField(blank=False)
    address = models.TextField(blank=False)
    stock = models.ManyToManyField(Item, related_name='shops')

    def __str__(self):
        return self.name

