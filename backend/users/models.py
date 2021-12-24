from django.db import models
import uuid


# Create your models here.
class Invitation(models.Model):
	public_id = models.UUIDField(
		default=uuid.uuid4,
		editable=False,
		unique=True
	)
	
	is_active = models.BooleanField(default=True)
