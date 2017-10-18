from . import fields


class MockPage(object):
    pk = None
    id = None

    def __init__(self, data):
        self.section = data[0].get('section', 1)
        self.questions = self._create_questions(data)

    def _create_questions(self, data):
        questions = []
        for question_data in data:
            question = MockQuestion(question_data)
            questions.append(question)
        return questions


class MockQuestion(object):

    def __init__(self, data):
        self.pk = self.id = data.get('id')
        self.text = data.get('question_text')
        self.type = data.get('type')
        self.section = data.get('section')
        self.position = data.get('position', 0)
        self.serialized = data
        self.choices = [
            MockChoice(choice_data)
            for choice_data in data.get('choices', [])
        ]

    @property
    def field_id(self):
        return 'question_' + str(self.id)

    @property
    def choices_field_display(self):
        return [
            (choice.pk, choice.text)
            for choice in self.choices
        ]

    def make_field(self):
        field_generator = getattr(
            fields.QuestionField,  # from the QuestionFields object
            self.type.lower(),  # get the field that correspond to the question type
            fields.QuestionField.singlelinetext,  # otherwise get a singlelinetext field
        )
        return field_generator(self)


class MockChoice(object):

    def __init__(self, data):
        self.pk = self.id = data.get('pk')
        self.text = data.get('text')
        self.position = data.get('position', 0)