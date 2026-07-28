import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from cdr.models import Thing, Device, Session
from core.models import Base
from .manager import MinUserManager



class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MinUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Profile(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255)
    celular = models.CharField(max_length=20, null=True, blank=True)
    thing = models.ForeignKey(
        Thing,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='things_profiles'
    )

    @property
    def qtd_devices_com_sessao(self):
        if not self.thing:
            return 0
        return Device.objects.filter(
            thing=self.thing
        ).filter(
            models.Exists(Session.objects.filter(device=models.OuterRef('pk')))
        ).count()

    @property
    def qtd_total_sessoes(self):
        if not self.thing:
            return 0
        return Session.objects.filter(device__thing=self.thing).count()

    def __str__(self):
        return f"Profile: {self.name}"
