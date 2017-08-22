import nested_admin

from .base import ChoiceInline, DowncastedAdmin


class FormQuestionAdminMixin(object):
    search_fields = ['text', 'descriptive_text']
    list_filter = ['page__sites']


class FormQuestionChildAdmin(
    FormQuestionAdminMixin,
    nested_admin.NestedModelAdmin
):
    list_display = ['short_str', 'page']


class MultipleChoiceParentAdmin(
    FormQuestionAdminMixin,
    DowncastedAdmin
):
    list_display = ['short_str', 'model_type', 'page']
    inlines = [ChoiceInline]


class MultipleChoiceChildAdmin(
    FormQuestionChildAdmin,
):
    inlines = [ChoiceInline]
