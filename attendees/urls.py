from django.urls import path    # path function -> defines URL patterns
from . import views             # imports all views from this app

# urlpatterns -> list of all URLs in this app
# each path() -> one URL that tells django the URL in browser and which function to run when someone visits URL
urlpatterns = [
    path('register/', views.register, name='register'),
    path('success/', views.success, name='success'),
]

# 'register/' -> the URL in the browser, example: http://127.0.0.1:8000/register/
# views.register -> the function in views.py that runs
# name='register' -> a shortcut name, instead of typing /register/ everywhere in code, you can use redirect('register') or {% url 'register' %} in templates
