from django.contrib import admin
from .models import Profile, CLanguage


# Register your models here.
admin.site.register(Profile)


@admin.register(CLanguage)
class ClangugeAdmin(admin.ModelAdmin):
    """Customizing  the way models are  displayed.."""

    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    prepopulated_fields = {'slug': ('title',)}  # AUTO MATICALLY FIELD SLUGE USEING TITILE
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
