from django.contrib import admin
from .models import Todo, Collection

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    pass

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass