from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Women, Category
# Register your models here.

class MarriedFilter(admin.SimpleListFilter):#для добавления СВОЕГО фильтра в панель фильтрации WomenAdmin list_filter =
    title = 'Статус женщин'
    parameter_name = 'status'

    def lookups(self, request, model_admin): #идут два метода. Первый lookups() должен возвращать список из возможных значений параметра status и названий позиций в панели фильтра
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем'),
        ]

    def queryset(self, request, queryset):#.  queryset() отвечает за отбор записей для соответствующей выбранной позиции
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)

@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'husband', 'tags']#поля, отображаемые в меню редактирования поста, порядок как в списке. Все обязательные для модели поля тут должны быть
    #exclude = ['tags', 'is_published'] #аналог поля fields только указываем все что НЕ НУЖНО при добавлении
    readonly_fields = ['post_photo']#нередактируемые поля
    prepopulated_fields = {"slug": ("title",)}#при создании объекта слаг формируется на основании заголовка
    filter_horizontal = ['tags']#удобный виджет для поля tags при создании объекта через админку
    #filter_vertical = ['tags']#удобный виджет для поля tags при создании объекта через админку
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('title',)
    ordering = ['time_create', 'title']#brief_info мы не можем явно указать, т.к. этот метод пользовательский, его как бы и нет в б.д модели
    list_editable = ('is_published', )
    list_per_page = 15
    actions = ['set_published', 'set_draft']#действия
    search_fields = ['title__startswith', 'cat__name']#поиск по полям, можно с лукапами, так как cat - это не обычное поле, а ключ к объекту модели Category, через __ обращаемся в полю name объекта Category
    list_filter = [MarriedFilter, 'cat__name', 'is_published']#панель фильтрации по полям  MarriedFilter - это свой пользовательский класс для фильтрации, просто класс
    save_on_top = True #кнопочка СОхранить вверху тоже

    # @admin.display(description="Краткое описание", ordering='content')#Обратите внимание, что мы не можем пользовательские поля указывать как сортируемые в коллекции ordering. Получим ошибку. Их сортировка может выполняться только на базе других существующих в таблице полей.
    # def brief_info(self, women: Women):
    #     return f"Описание {len(women.content)} символов."

    @admin.display(description="Изображение")
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")#mark_safe нужна, чтобы тэги не экранировались
        return "Без фото"

    @admin.action(description="Опубликовать выбранные записи")# нужно, чтобы в админке set_published выглядел как "Опубликовать выбранные записи"
    def set_published(self, request, queryset):#выбрать галочками записи и изменить для всех выбранных 'is_published' на ОПУБЛИКОВАНО
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")# сообщение об успешном опубликовании N-го кол-ва записей

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!", messages.WARNING)




#admin.site.register(Women, WomenAdmin) аналогично использованию @admin.register(Women)/class WomenAdmin(admin.ModelAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')



