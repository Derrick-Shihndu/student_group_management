from django.contrib import admin
from .models import MainGroup, SubGroup, Student, Course, GroupNote, GroupMessage

class SubGroupInline(admin.TabularInline):
    model = SubGroup
    extra = 0

class CourseInline(admin.TabularInline):
    model = Course
    extra = 0

@admin.register(MainGroup)
class MainGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_members', 'created_at', 'delegate_phone')
    inlines = [SubGroupInline, CourseInline]
    search_fields = ('name',)

@admin.register(SubGroup)
class SubGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_group', 'leader')
    search_fields = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_group')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name1','name2','phone','subgroup','joined_at')
    search_fields = ('name1','name2','phone','email')

@admin.register(GroupNote)
class GroupNoteAdmin(admin.ModelAdmin):
    list_display = ('title','subgroup','posted_at')

@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ('subgroup','posted_at')
