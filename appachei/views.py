from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Usuario, ObjetoIdentificado
import qrcode
from io import BytesIO
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.core.files.base import ContentFile
from django.urls import reverse

def home(request):
    return render(request, 'home.html')

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data_nascimento = request.POST.get('data_nascimento')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Validar email
        if not email or '@' not in email:
            return HttpResponse('E-mail inválido. Por favor, insira um endereço de e-mail válido.')
        
        # Verifica se o email já está cadastrado
        if Usuario.objects.filter(email=email).exists():
            return HttpResponse('E-mail já cadastrado. Por favor, faça o login ou cadastre outro e-mail.')
        
        # Cria novo usuário
        usuario = Usuario.objects.create_user(nome=nome, data_nascimento=data_nascimento, email=email, password=senha)
        
        # Gera e salva o QRCode para o novo usuário
        gerar_qr_code(usuario, request)
        
        # Autentica e faz login
        user = authenticate(request, username=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect('perfil')
   
    return render(request, 'cadastro.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = authenticate(request, username=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect('perfil')
        else:
            return render(request, 'login.html', {'error': 'E-mail ou senha inválidos.'})
        
    return render(request, 'login.html')

@login_required
def perfil(request):
    usuario = request.user
    qr_code_url = usuario.qr_code.url if usuario.qr_code else None
    return render(request, 'perfil.html', {'username': usuario.nome, 'qr_code_url': qr_code_url})
    
def logout_view(request):
    logout(request)
    return redirect('home')

def objeto_encontrado(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        mensagem = request.POST.get('mensagem')
        contato = request.POST.get('contato')

        send_mail(
            subject='Objeto encontrado!',
            message=f'Olá, {usuario.nome}, \n\nVocê recebeu uma mensagem da pessoa que encontrou seu objeto perdido.\nAo combinar a devolução, marque o encontro em locais públicos e movimentados, para sua segurança e da pessoa que está devolvendo.\n\nMensagem: {mensagem}\nContato: {contato}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[usuario.email],
            fail_silently=False,       
        )

        return render(request, 'objeto_encontrado.html', {'message_sent': True})
    
    return render(request, 'objeto_encontrado.html', {'usuario': usuario})


def obrigado(request):
    return render(request, 'obrigado.html')

def gerar_qr_code(usuario, request):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    url_objeto_encontrado = request.build_absolute_uri(reverse('objeto_encontrado', args=[usuario.id]))
    qr.add_data(url_objeto_encontrado)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    usuario.qr_code.save(f'qr_code_{usuario.email}.png', ContentFile(buffer.getvalue()))

    return usuario.qr_code.url

def objetos_cadastrados(request):
    objetos = ObjetoIdentificado.objects.filter(usuario=request.user)
    return render(request, 'objetos_cadastrados.html', {'objetos': objetos})

def salvar_objeto(request):
    if request.method == 'POST':
        objeto_nome = request.POST.get('objeto')
        if objeto_nome:
            objeto = ObjetoIdentificado.objects.create(usuario=request.user, nome=objeto_nome)
            objeto.save()
            return redirect('objetos_cadastrados')
        return render(request='formulario.html')
    
def pagina_sucesso(request):
    return render(request, 'pagina_sucesso.html')

@login_required
def apagar_objeto(request, objeto_id):
    objeto = get_object_or_404(ObjetoIdentificado, id=objeto_id)

    if request.user != objeto.usuario:
        return HttpResponseForbidden("Você não tem permissão para excluir este objeto.")
    
    objeto.delete()
    return redirect('objetos_cadastrados')

def quemsomos(request):
    return render(request, 'quemsomos.html')

def projeto(request):
    return render(request, 'projeto.html')

def saibamais(request):
    return render(request, 'saibamais.html')
