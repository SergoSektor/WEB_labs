from django.contrib import admin
from .models import ComputerScienceConcept, FieldOfStudy, ConceptDetail, Tag

admin.site.register(ComputerScienceConcept)
admin.site.register(FieldOfStudy)
admin.site.register(ConceptDetail)
admin.site.register(Tag)
