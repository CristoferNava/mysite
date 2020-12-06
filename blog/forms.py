from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25) # rendered as <input type="text">
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    # Each field has a default widget that determines how the field is rendered
    # in HTML

class CommentForm(forms.ModelForm):
    # To create a form from a model, we just need to indicate which model to use
    # to build the form in the Meta class of the form. Django introspects the model
    # and builds the form dynamically for us.
    class Meta:
        model = Comment
        # By default, Django builds a form field for each field contained in the model.
        # However, we can explicitly tell the framewoek which fields we want to include
        # in the form using fields 
        fields = ('name', 'email', 'body')