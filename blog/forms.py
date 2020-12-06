from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25) # rendered as <input type="text">
    email = forms.EmailField()
    to = forms.EmailField()
    commnents = forms.CharField(required=False, widget=forms.Textarea)
    # Each field has a default widget that determines how the field is rendered
    # in HTML