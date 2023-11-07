from django.forms import ModelForm
from .models import Project, Review
from django import forms


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'featured_image',
            'description',
            'demo_link',
            'source_code',
            'tags'

        ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),

        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class reviewform(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

    labels = {
        'value': 'choose your vote',
        'body': 'add comment'
    }

    def __init__(self, *args, **kwargs):
        super(reviewform, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
