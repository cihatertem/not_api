from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import Profile, Note, Category, MyUser

admin.site.register(MyUser, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ('owner', 'username', 'created_at')
    list_display_links = ('owner',)
    list_filter = ('created_at', 'owner')
    search_fields = ('owner', 'username', 'email')
    list_per_page = 25


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ('title', 'category', 'owner', 'created_at', 'is_pinned')
    list_display_links = ('title',)
    list_filter = ('created_at', 'owner', 'is_pinned')
    list_editable = ('is_pinned',)
    search_fields = ('owner', 'title', 'category', 'body')
    list_per_page = 25


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    list_display = ('name', 'owner', 'created_at')
    list_display_links = ('name',)
    list_filter = ('created_at', 'owner')
    search_fields = ('owner', 'name')
    list_per_page = 25
