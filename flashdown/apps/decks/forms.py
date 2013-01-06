from django import forms
from apps.decks.models import Deck
from crispy_forms.helper import FormHelper

MAX_DESC_LEN = 500

class DeckForm(forms.ModelForm):

    class Meta:
        model = Deck
        fields = ('name', 'description', 'private', 'tags')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5,
                                                 'maxlength': MAX_DESC_LEN})
        }

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

    def clean_description(self):
        desc = self.cleaned_data.get('description', None)
        if desc is not None and len(desc) > MAX_DESC_LEN:
            raise forms.ValidationError("Must be less than %d characters." % MAX_DESC_LEN)

        return desc



