from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(models.Model):

    name = models.CharField(
        verbose_name='Название товара',
        max_length=30,
        unique=True
    )
    description = models.TextField(
        verbose_name='Описание товара',
        blank=True
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
    )
    
    created_at = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    updated_at = models.DateField(
        verbose_name='Дата обновления',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Review(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name="Текст отзыва"
    )
    rating = models.SmallIntegerField(
        verbose_name="Оценка",
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    updated_at = models.DateField(
        verbose_name='Дата обновления',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.text}, {self.rating}'


class Order(models.Model):

    NEW = 'NEW'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'

    STATUS_CHOICES = [
        (NEW, 'Новый'),
        (IN_PROGRESS, 'В работе'),
        (DONE, 'Выполнен')
    ]

    user = models.ForeignKey(
        User,
        verbose_name='Заказчик',
        on_delete=models.CASCADE
    )

    positions = models.ManyToManyField(
        Product,
        through='OrderedProducts'
    )

    status = models.CharField(
        verbose_name='Статус заказа',
        max_length=11,
        choices=STATUS_CHOICES,
        default=NEW
    )

    total_price = models.PositiveIntegerField(
        verbose_name='Общая сумма заказа',
        default=1
    )

    created_at = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    updated_at = models.DateField(
        verbose_name='Дата обновления',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ пользователя {self.user} на сумму {self.total_price}'


class OrderedProducts(models.Model):

    order = models.ForeignKey(
        Order,
        related_name='ordered_products',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        verbose_name='Количество товара'
    )


class Collection(models.Model):

    title = models.CharField(
        max_length=40,
        verbose_name='Заголовок',
        unique=True
    )

    text = models.TextField(
        verbose_name='Текст'
    )

    products = models.ManyToManyField(
        Product,
        related_name='collections',
        verbose_name='Товары в подборке'
    )

    created_at = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    updated_at = models.DateField(
        verbose_name='Дата обновления',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'

    def __str__(self):
        return self.title
