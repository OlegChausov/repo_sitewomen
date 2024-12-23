

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]


class DataMixin:
    paginate_by=5
    title_page = None
    cat_selected = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.cat_selected is not None: # именно Not None, а не True, т.к. 0 не вернет True, но для нас он допустимое нормальное значение
            self.extra_context['cat_selected'] = self.cat_selected
        ##функционал может быть заменен на {% block mainmenu %} women_tags.py/get_menu()
        # функционал заменен на context_pricessors.py get_menu
        # if 'menu' not in self.extra_context:
        #     self.extra_context['menu'] = menu

    def get_mixin_context(self, context, **kwargs):
        # context['menu'] = menu #функционал может быть заменен на {% block mainmenu %} women_tags.py/get_menu()
        # функционал заменен на context_pricessors.py get_menu
        context['cat_selected'] = None
        context.update(kwargs)
        return context

