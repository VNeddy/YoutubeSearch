from django import forms

class SearchForm(forms.Form):
    keyword = forms.CharField(min_length=1, label="keyword", error_messages={"required": "关键字不能为空!"})
    order = forms.CharField(label="order")
    scope_start = forms.CharField(label="scope_start")
    scope_end = forms.CharField(label="scope_end")
    maxResult = forms.CharField(label="maxResult")
