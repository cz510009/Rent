from django import forms
from django.contrib.auth.forms import UserCreationForm

class LowerChoiceForm(forms.Form):
    lower = forms.fields.ChoiceField(
        choices=(
            ('0', '下限なし'),
            ('3', '3万円以上'),
            ('4', '4万円以上'),
            ('5', '5万円以上'),
            ('6', '6万円以上'),
            ('7', '7万円以上'),
            ('8', '8万円以上'),
            ('9', '9万円以上'),
            ('10', '10万円以上'),
            ('11', '11万円以上'),
            ('12', '12万円以上')
        ),
        required=True,
        widget=forms.widgets.Select
    )


class UpperChoiceForm(forms.Form):
    upper = forms.fields.ChoiceField(
        choices=(
            ('0', '上限なし'),
            ('3', '3万円以下'),
            ('4', '4万円以下'),
            ('5', '5万円以下'),
            ('6', '6万円以下'),
            ('7', '7万円以下'),
            ('8', '8万円以下'),
            ('9', '9万円以下'),
            ('10', '10万円以下'),
            ('11', '11万円以下'),
            ('12', '12万円以下')
        ),
        required=True,
        widget=forms.widgets.Select
    )


class TimeChoiceForm(forms.Form):
    time = forms.fields.ChoiceField(
        choices=(
            ('0', '指定なし'),
            ('5', '5分以内'),
            ('10', '10分以内'),
            ('15', '15分以内'),
            ('20', '20分以内'),

        ),
        required=True,
        widget=forms.widgets.Select
    )

class LowerAreaChoiceForm(forms.Form):
    lowerArea = forms.fields.ChoiceField(
        choices=(
            ('0', '下限なし'),
            ('20', '20㎡以上'),
            ('25', '25㎡以上'),
            ('30', '30㎡以上'),
            ('35', '35㎡以上'),
            ('40', '40㎡以上'),
            ('45', '45㎡以上'),
            ('50', '50㎡以上'),
            ('55', '55㎡以上'),
            ('60', '60㎡以上'),
        ),
        required=True,
        widget=forms.widgets.Select
    )

class UpperAreaChoiceForm(forms.Form):
    upperArea = forms.fields.ChoiceField(
        choices=(
            ('0', '上限なし'),
            ('20', '20㎡以下'),
            ('25', '25㎡以下'),
            ('30', '30㎡以下'),
            ('35', '35㎡以下'),
            ('40', '40㎡以下'),
            ('45', '45㎡以下'),
            ('50', '50㎡以下'),
            ('55', '55㎡以下'),
            ('60', '60㎡以下'),
        ),
        required=True,
        widget=forms.widgets.Select
    )

class AgeChoiceForm(forms.Form):
    age = forms.fields.ChoiceField(
        choices=(
            ('0', '指定なし'),
            ('5', '5年以内'),
            ('10', '10年以内'),
            ('15', '15年以内'),
            ('20', '20年以内'),
            ('25', '25年以内'),
        ),
        required=True,
        widget=forms.widgets.Select
    )


