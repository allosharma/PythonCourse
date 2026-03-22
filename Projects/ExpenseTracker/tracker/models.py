from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Transaction(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # date = models.DateField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.description} - {self.amount}"