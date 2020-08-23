from django import forms


class CreateForm(forms.Form):
    title = forms.CharField(label='Title', max_length=50)
    content = forms.CharField(widget=forms.Textarea, label='Content')