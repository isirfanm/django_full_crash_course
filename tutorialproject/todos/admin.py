from django.contrib import admin

from todos.models import Person, Todo

# admin.site.register(Todo)
admin.site.register(Person)


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'deadline', 'done')
    list_filter = ('deadline', 'priority')
    search_fields = ('title',)
