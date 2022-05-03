from django_filters.filters import CharFilter
from django import forms


def inverse_choices(choices):
    return {choice[1]: choice[0] for choice in choices}


class CareChoiceFilter(CharFilter):
    def __init__(self, *args, **kwargs):
        if "choice_dict" in kwargs:
            self.choice_dict = kwargs.pop("choice_dict")
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        if len(value) > 0:
            value = self.choice_dict.get(value)
        return super().filter(qs, value)

