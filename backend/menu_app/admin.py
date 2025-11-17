from django.contrib import admin

from .models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ('title', 'url', 'named_url', 'parent', 'order')
    raw_id_fields = ('parent',)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = (MenuItemInline,)
