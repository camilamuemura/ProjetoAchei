from django.urls import path
from .views import home, cadastro, login_view, perfil, logout_view, objeto_encontrado, obrigado, objetos_cadastrados, salvar_objeto, pagina_sucesso, apagar_objeto, projeto, quemsomos, saibamais


urlpatterns = [
    path('', home, name='home'),
    path('cadastro/', cadastro, name='cadastro'),
    path('login/', login_view, name='login'),
    path('perfil/', perfil, name='perfil'),
    path('logout/', logout_view, name='logout'),
    path('objeto-encontrado/<int:usuario_id>/', objeto_encontrado, name='objeto_encontrado'),
    path('obrigado/', obrigado, name='obrigado'),
    path('objetos_cadastrados/', objetos_cadastrados, name='objetos_cadastrados'),
    path('salvar_objeto/', salvar_objeto, name='salvar_objeto'),
    path('pagina_sucesso/', pagina_sucesso, name='pagina_sucesso'),
    path('apagar_objeto/<int:objeto_id>/', apagar_objeto, name='apagar_objeto'),
    path('quemsomos/', quemsomos, name='quemsomos'),
    path('projeto/', projeto, name='projeto'),
    path('saibamais/', saibamais, name='saibamais'),

]