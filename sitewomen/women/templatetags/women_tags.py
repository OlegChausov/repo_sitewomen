from django import template
import women.views as views
from women.models import Category

register = template.Library()

#@register.simple_tag(name='getcats')  #name объявлять не обязательно, можно использовать название тега при объявлении def
#def get_categories():
#    return views.cats_db

#@register.inclusion_tag('women/list_categories.html')
#def show_categories(cat_selected=0):
#    cats = views.cats_db #в принципе, лишняя переменная
#    return {"cats": cats, "cat_selected": cat_selected} #можно так return {"cats": views.cats_db, "cat_selected": cat_selected}

@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected_id=0):
    cats = Category.objects.all()
    return {"cats": cats, "cat_selected": cat_selected_id}