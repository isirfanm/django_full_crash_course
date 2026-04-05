from django import forms

from todos.models import Todo


class PersonForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Your Name")
    age = forms.IntegerField(required=True, label="Your Age")
    job = forms.CharField(required=False, label="Your Job")


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "description", "done", "deadline", "priority"]

        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }
