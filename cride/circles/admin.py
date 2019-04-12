"""Circle models admin."""

# Django
from django.contrib import admin
from django.urls import path
from django.shortcuts import render

# Models
from cride.circles.models import Circle

# Forms
from .forms import UploadFileForm

# Utilities
import csv
from io import TextIOWrapper


@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    """Circle model admin."""

    list_display = (
        'slug_name',
        'name',
        'is_public',
        'verified',
        'is_limited',
        'members_limit'
    )
    search_fields = ('slug_name', 'name')
    list_filter = (
        'is_public',
        'verified',
        'is_limited'
    )

    actions = ['make_verified', 'make_unverified']

    def make_verified(self, request, queryset):
        """Make circles verified."""
        queryset.update(verified=True)

    make_verified.short_description = 'Make selected circles verified'

    def make_unverified(self, request, queryset):
        """Make circles unverified."""
        queryset.update(verified=False)

    make_unverified.short_description = 'Make selected circles unverified'

    def get_urls(self):
        urls = super(CircleAdmin, self).get_urls()
        custom_urls = [
            path('import-csv/', self.import_csv)
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                self.handle_import_csv(request.FILES['file'])
                self.message_user(request, "Your csv file has been imported")
        else:
            form = UploadFileForm()
        return render(request, 'admin/circles/circle/csv_form.html', {'form': form})

    def handle_import_csv(self, f):
        # For more information:
        # https://stackoverflow.com/questions/16243023/how-to-resolve-iterator-should-return-strings-not-bytes
        file = TextIOWrapper(f.file, encoding='utf-8')
        reader = csv.DictReader(file)
        for row in reader:
            circle = Circle(**row)
            circle.save()
