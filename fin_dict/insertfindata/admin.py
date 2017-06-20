# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from insertfindata.models import Section,SubSection,SubSubSubsection,SubSubSection
# Register your models here.

admin.site.register(Section)
admin.site.register(SubSection)
admin.site.register(SubSubSubsection)
admin.site.register(SubSubSection)