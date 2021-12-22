from django.db import models


# Create your models here.
class Test(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name


class Question(models.Model):
	title = models.CharField(max_length=255,)
	test = models.ForeignKey(
		Test,
		related_name="questions",
		on_delete=models.CASCADE
	)

	def __str__(self):
		return f"{self.test.name} => {self.title}"


class Option(models.Model):
	answer = models.CharField(max_length=255,)
	question = models.ForeignKey(
		Question,
		related_name="options",
		on_delete=models.CASCADE
	)

	is_true = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.question.title} => {self.answer}"
