from django.db.models.signals import post_save  # signalas (būna įvairių)
from django.contrib.auth.models import User     # siuntėjas
from django.dispatch import receiver            # priėmėjas (dekoratorius)
from .models import Profile

# Sukūrus vartotoją automatiškai sukuriamas ir profilis.
@receiver(post_save, sender=User) # jeigu išsaugojamas User objektas, inicijuojama f-ja po dekoratoriumi
def create_profile(sender, instance, created, **kwargs): # instance yra ką tik sukurtas User objektas.
    """
    Create a profile if a User instance was created.
    If the User object is save, this function will be called.
    :param sender: User model class
    :param instance: created specific instance of Profile
    :param created: boolean whether User was created
    :param kwargs:
    :return:
    """
    if created:
        Profile.objects.create(user=instance)
        print('KWARGS: ', kwargs)


# Pakoregavus vartotoją, išsaugomas ir profilis
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()