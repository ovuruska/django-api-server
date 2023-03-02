# utils.py
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Transaction

@receiver(pre_delete, sender=Transaction)
def delete_old_transactions(sender, **kwargs):
    one_week_ago = timezone.now() - timezone.timedelta(seconds=10)
    Transaction.objects.filter(created_at=one_week_ago).delete()
