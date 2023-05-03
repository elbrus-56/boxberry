import uuid
from django.db import models


class UUIDModel(models.Model):
    """Абстрактная модель для uuid."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStamp(models.Model):
    """Абстрактная модель с меткой времени"""

    created_at = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, null=True, verbose_name="Дата последнего изменения"
    )

    class Meta:
        abstract = True
