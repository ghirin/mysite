# Импорт модуля forms из Django для создания форм
from django import forms

# Импорт модели Comment из models.py
from .models import Comment

# Создание класса формы для отправки поста по email
class EmailPostForm(forms.Form):
    """
    Форма для отправки рекомендации поста по электронной почте.
    Наследуется от базового класса forms.Form.
    """
    
    # Поле для имени отправителя
    name = forms.CharField(
        max_length=25,  # Максимальная длина 25 символов
        # Необязательные параметры, которые можно добавить:
        label='Ваше имя',  # Подпись поля
        # widget=forms.TextInput(attrs={'class': 'form-control'})  # HTML-атрибуты
    )
    
    # Поле для email отправителя
    email = forms.EmailField(
        # Автоматически проверяет валидность email-адреса
        # Дополнительные параметры:
        label='Ваш email',
        # help_text='Мы никому не передадим ваш email'
    )
    
    # Поле для email получателя
    to = forms.EmailField(
        label='Электронная почта получателя',  # Кастомная метка поля
        # Можно добавить валидаторы:
        # validators=[validate_email_domain]  # Проверка домена получателя
    )
    
    # Поле для дополнительных комментариев (необязательное)
    comments = forms.CharField(
        required=False,  # Поле не обязательно для заполнения
        widget=forms.Textarea,  # Используем textarea вместо input
        # Дополнительные параметры:
        label='Комментарий (необязательно)',
        # attrs={'rows': 4, 'placeholder': 'Ваш комментарий...'}
    )
    
    # Метод clean для кастомной валидации (пример)
    # def clean(self):
    #     cleaned_data = super().clean()
    #     if cleaned_data.get('email') == cleaned_data.get('to'):
    #         raise forms.ValidationError("Нельзя отправлять письмо самому себе")
    #     return cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        labels = {
            'name': 'Ваше имя',
            'email': 'Ваш email',
            'body': 'Ваш комментарий',
        }

class SearchForm(forms.Form):
    query = forms.CharField(
        label='Поиск',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Введите текст для поиска'})
    )

# Ключевые особенности:
# Базовые поля формы:
# CharField - для текстовых данных
# EmailField - с автоматической валидацией email-адреса
# Параметр max_length ограничивает длину ввода
# Необязательные поля:
# required=False делает поле комментариев необязательным
# По умолчанию все поля обязательные (required=True)
# Виджеты (Widgets):
# Textarea преобразует поле в <textarea> HTML-элемент
# По умолчанию CharField использует <input type="text">
# Расширенные возможности:
# Кастомные метки (label)
# Подсказки (help_text)
# HTML-атрибуты через attrs
# Валидаторы (validators)
# Метод clean() для комплексной проверки данных
# Безопасность:
# Автоматическая экранирование HTML-тегов
# Проверка CSRF при использовании в шаблонах
# Валидация данных перед использованием
# Использование в представлении:
# form = EmailPostForm(request.POST or None)
# if form.is_valid():
#     # Обработка валидных данных
#     cd = form.cleaned_data  # Доступ к очищенным данным
# Эта форма обеспечивает:
# Структурированный ввод данных
# Встроенную валидацию
# Гибкость настройки отображения
# Безопасную обработку пользовательского ввода
