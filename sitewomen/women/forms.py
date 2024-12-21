from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils.deconstruct import deconstructible


from .models import Category, Husband, Women


@deconstructible
class RussianValidator: #создаем свой валидатор
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code, params={"value": value})

# class AddPostForm(forms.Form): #форма не связана с моделью
#     title = forms.CharField(max_length=255, min_length=5, label="Заголовок",
#                             widget=forms.TextInput(attrs={'class': 'form-input'}),
#                             validators=[RussianValidator(),], #пользовательский валидатор
#                             error_messages={
#                                 'min_length': 'Слишком короткий заголовок',
#                                 'required': 'Без заголовка - никак',
#                             })#виджет указывает на доп. атрибуты,например CSS поля ввода; error_messages - словарь{название валидатора: сообщение при его нарушении}
#     slug = forms.SlugField(max_length=255, label="URL", validators=[
#         MinLengthValidator(5, message="Минимум 5 символов"),
#         MaxLengthValidator(100, message="Максимум 100 символов"),
#     ])#переопределяем валидаторы от валидаторов базового класса на свои собственные
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label="Контент")#виджет указывает на доп. атрибуты,например размер поля ввода
#     is_published = forms.BooleanField(required=False, initial=True, label="Статус")
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")
#     husband = forms.ModelChoiceField(queryset=Husband.objects.all(), empty_label="Не замужем", required=False, label="Муж")
#
#     def clean_title(self): # будет вызываться проверка clean_нужное поле формы, это как замена своему классу валидатора. Для использолвания в одном месте
#         title = self.cleaned_data['title'] #все методы с ключевым словом cleaned вызываются автоматически при созадния экземпляра класса формы
#         ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
#         if not (set(title) <= set(ALLOWED_CHARS)):
#             raise ValidationError("Должны быть только русские символы, дефис и пробел.")
#
#         return title


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")#эти поля нужны, чтобы указать параметр значения по умолчанию в форме
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), empty_label="Не замужем", required=False,label="Муж")#эти поля нужны, чтобы указать параметр значения по умолчанию в форме

    class Meta:
        model = Women
        #fields = '__all__' #в форме появятся все поля модели, заполняемых автоматический, заголовок поля формы будет verbouse_name модели
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']#лучше указать явно
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})}#виджеты с параметрами стилей
        labels = {'slug': 'URL'}#переопределим заголовок с verbouse_name на свой

    def clean_title(self): #все методы с ключевым словом cleaned вызываются автоматически при созадния экземпляра класса формы
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')

        return title

class UploadFileForm(forms.Form):
    #file = forms.FileField(label="Файл", required=False)
    file = forms.ImageField(label="Изображение", required=False)
