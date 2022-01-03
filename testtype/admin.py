from django.contrib import admin
from .models import TestType


# Register your models here.

def make_test_enabled(modeladmin, request, queryset):
    queryset.update(status='enabled')


def make_test_disabled(modeladmin, request, queryset):
    queryset.update(status='disabled')


make_test_enabled.short_description = 'Make all test enabled'
make_test_disabled.short_description = 'Make all test disabled'


class TesttypeDetails(admin.ModelAdmin):
    list_display = ('disease_name', 'status')
    list_editable = ('status',)
    search_fields = ('disease_name',)
    list_filter = ('status',)
    actions = [make_test_enabled, make_test_disabled]


admin.site.register(TestType, TesttypeDetails)
