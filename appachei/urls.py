from django.urls import path
from .views import home, cadastro, login_view, perfil, logout_view, objeto_encontrado, obrigado


urlpatterns = [
    path('', home, name='home'),
    path('cadastro/', cadastro, name='cadastro'),
    path('login/', login_view, name='login'),
    path('perfil/', perfil, name='perfil'),
    path('logout/', logout_view, name='logout'),
    path('objeto-encontrado/<int:usuario_id>/', objeto_encontrado, name='objeto_encontrado'),
    path('obrigado/', obrigado, name='obrigado'),
]