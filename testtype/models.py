from random import choice

from django.db import models


# Create your models here.
class TestType(models.Model):
    class Meta:
        db_table = 'test_type_table'

    ENABLED = 'enabled'
    DISABLED = 'disabled'
    status_choice = ((ENABLED, 'enable'), (DISABLED, ('disable')))

    disease_name = models.CharField(max_length=150, unique=True)
    status = models.CharField(choices=status_choice, max_length=10, default=DISABLED)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % (self.disease_name)
