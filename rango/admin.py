from django.contrib import admin
from rango.models import Category, Page, UserProfile


class PageInline(admin.TabularInline):
    model = Page
    extra = 3


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')
    fieldsets = [
        ('Title:', {'fields': ['title']}),
        ('Category:', {'fields': ['category']}),
        (None, {'fields': ['url']}),
        (None, {'fields': ['views']}),
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'views', 'likes')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PageInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
