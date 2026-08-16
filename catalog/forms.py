from django import forms


class ContactForm(forms.Form):
    SUBJECT_CHOICES = [
        ("", "Choisir un sujet"),
        ("general", "Question générale"),
        ("niveau", "Suggestion de niveau"),
        ("feedback", "Retour sur la plateforme"),
        ("partenariat", "Partenariat"),
        ("autre", "Autre"),
    ]

    name = forms.CharField(
        label="Votre nom",
        max_length=120,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Votre nom complet",
                "autocomplete": "name",
            }
        ),
    )
    email = forms.EmailField(
        label="Adresse email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "vous@exemple.com",
                "autocomplete": "email",
            }
        ),
    )
    phone = forms.CharField(
        label="Téléphone",
        required=False,
        max_length=40,
        widget=forms.TextInput(
            attrs={
                "placeholder": "+243 …",
                "autocomplete": "tel",
            }
        ),
    )
    subject = forms.ChoiceField(
        label="Sujet",
        choices=SUBJECT_CHOICES,
        widget=forms.Select(),
    )
    message = forms.CharField(
        label="Message",
        min_length=10,
        max_length=2000,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Écrivez votre message…",
                "rows": 5,
            }
        ),
    )

    def clean_subject(self):
        subject = self.cleaned_data.get("subject", "")
        if not subject:
            raise forms.ValidationError("Veuillez choisir un sujet.")
        return subject
