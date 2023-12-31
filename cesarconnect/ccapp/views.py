from django.shortcuts import render, redirect
from .models import Pessoa
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required

# Create your views here.

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            pessoa = Pessoa.objects.get(email=email, senha=senha)
            request.session['pessoa_id'] = pessoa.id_usuario
            return redirect('tela_inicial')
        except Pessoa.DoesNotExist:
            return render(request, "senhaincorreta.html")


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if Pessoa.objects.filter(email=email).exists():
            return render(request, "emailinvalido.html")
        
        novo_usuario = Pessoa()
        novo_usuario.nome = username
        novo_usuario.email = email
        novo_usuario.senha = senha
        novo_usuario.save()

        try:
            pessoa = Pessoa.objects.get(email=email, senha=senha)
            request.session['pessoa_id'] = pessoa.id_usuario
            return redirect('tela_inicial')
        except Pessoa.DoesNotExist:
            return render(request, "senhaincorreta.html")
    
        

def tela_inicial(request):
    if 'pessoa_id' in request.session:
        pessoa_id = request.session['pessoa_id']
        pessoa = Pessoa.objects.get(id_usuario=pessoa_id)
        nome_usuario = pessoa.nome
        context = {
            'nome_usuario': nome_usuario
        }
        return render(request, 'tela_inicial.html', context)
    else:
        return redirect('login')

def criargrupo(request):
    return render(request, 'criargrupo.html')

def meugrupo(request):
    return render(request, 'meugrupo.html')

def acessarperfil(request):
    if 'pessoa_id' in request.session:
        pessoa_id = request.session['pessoa_id']
        pessoa = Pessoa.objects.get(id_usuario=pessoa_id)
        nome_usuario = pessoa.nome
        context = {
            'nome_usuario': nome_usuario
        }
        return render(request, 'acessarperfil.html', context)

def editar_perfil(request):
    return render(request, 'editar_perfil.html')

def emailinvalido(request):
    return render(request, 'emailinvalido.html')

def senhaincorreta(request):
    return render(request, 'senhaincorreta.html')