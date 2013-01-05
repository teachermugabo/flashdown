from django import forms
from apps.decks.models import Deck

from crispy_forms.helper import FormHelper

class DeckForm(forms.ModelForm):

    class Meta:
        model = Deck
        fields = ('name', 'description', 'private', 'tags')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.help_text_inline = True
        self.helper.error_text_inline = True
        super(DeckForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name', None)
        try:
            Deck.objects.get(name=name, active=True)
        except Deck.DoesNotExist:
            return name

        raise forms.ValidationError("Deck with that name already exists.")


