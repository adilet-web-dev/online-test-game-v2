from rest_framework.serializers import ModelSerializer
from django.db import transaction

from cubes.models import Test, Question, Option


class OptionSerializer(ModelSerializer):
	class Meta:
		model = Option
		fields = ['answer', 'is_true']


class QuestionSerializer(ModelSerializer):
	options = OptionSerializer(many=True)

	class Meta:
		model = Question
		fields = ['title', 'options']


class TestSerializer(ModelSerializer):
	questions = QuestionSerializer(many=True)

	def _save_questions_and_options(self, validated_data, test: Test):
		for question in validated_data.get('questions'):
			q = Question.objects.create(title=question.get('title'), test=test)
			for option in question.get('options'):
				Option.objects.create(
					is_true=option.get('is_true'),
					answer=option.get('answer'),
					question=q
				)

	def create(self, validated_data):
		test = Test.objects.create(name=validated_data.get('name'))
		self._save_questions_and_options(validated_data, test)

		return test

	@transaction.atomic
	def update(self, instance: Test, validated_data):

		instance.questions.all().delete()
		instance.name = validated_data.get('name')
		instance.save()
		self._save_questions_and_options(validated_data, instance)

		return instance

	class Meta:
		model = Test
		depth = 2
		fields = ['id', 'name', 'questions']
