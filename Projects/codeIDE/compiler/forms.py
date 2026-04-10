from django import forms


class CodeSubmissionForm(forms.Form):
    code = forms.CharField(max_length=20000, strip=False)
    stdin = forms.CharField(required=False, max_length=5000, strip=False)
