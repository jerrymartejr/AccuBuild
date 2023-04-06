from django.contrib import admin

from . models import User, Project, Division, DivisionCost, Client, Scope, ItemType, Item

# Register your models here.

admin.site.register(User)
# admin.site.register(Project)
admin.site.register(Division)
admin.site.register(DivisionCost)
admin.site.register(Client)
admin.site.register(Scope)
admin.site.register(ItemType)
admin.site.register(Item)


class DivisionInline(admin.TabularInline):
    model = Division.project.through
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    inlines = [DivisionInline]

admin.site.register(Project, ProjectAdmin)
