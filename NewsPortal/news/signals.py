from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from .tasks import new_post_subscription

@receiver(m2m_changed, sender=PostCategory)
def notify_subscriber(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        new_post_subscription(instance)
        