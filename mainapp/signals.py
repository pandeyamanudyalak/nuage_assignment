import logging
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

logger = logging.getLogger('django')


@receiver(post_migrate)
def create_initial_user(sender, **kwargs):
    User = get_user_model()  
    email = 'adminuser@example.com'
    password = 'adminpassword'
    if not User.objects.filter(email=email).exists():
        User.objects.create_user(
            email='adminuser@example.com',
            full_name='Admin User',
            username='adminuser',
            password=password
        )
        logger.info(f'Initial user created with\n email: {email} \n password: {password} \n \n \n \n \n \n \n\n\n\n\n\n\n')

