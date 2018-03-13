from rest_framework import serializers
from django.forms import ModelForm
from DataExtraction.models import *

class CompanyListForm(ModelForm):
    class Meta:
        model = CompanyList
        fields = ('company_name','ditname')