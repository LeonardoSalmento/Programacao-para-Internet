from django.shortcuts import render
from perfis.models import *
from django.shortcuts import redirect
from perfis.forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.core.paginator import Paginator, InvalidPage



# Create your views here.

@login_required
def index(request):
	form = PostForm()
	perfil_logado = Perfil.objects.get(id=request.user.perfil.id)
	perfis_nao_bloqueados = perfil_logado.contatos_nao_bloqueados
	
	page = request.GET.get("page", 1)
	paginator = Paginator(perfil_logado.minha_timeline.get_timeline(), 10)
	total = paginator.count
	
	try:
		timeline = paginator.page(page)
	except InvalidPage:
		timeline = paginator.page(1)
		
	contexto = {
		'perfis' : perfis_nao_bloqueados,
		'perfil_logado' : get_perfil_logado(request),
		'form':form,
		'timeline':timeline
		}
		
	return render(request, 'index.html', contexto)


@login_required
def exibir_perfil(request, perfil_id):
	perfil = Perfil.objects.get(id=perfil_id)
	perfil_logado = get_perfil_logado(request)
	posso_convidar = perfil_logado.pode_convidar(perfil)
	posso_bloquear = perfil_logado.pode_bloquear(perfil)
	posso_exibir = perfil_logado.pode_exibir(perfil)

	contexto = {'perfil' : perfil, 
				'perfil_logado' : perfil_logado,
				'posso_convidar': posso_convidar,
				'posso_bloquear': posso_bloquear, 
				'posso_exibir': posso_exibir
				}

	return render(request, 'perfil.html', contexto)
		          


@login_required
def convidar(request,perfil_id):

	perfil_a_convidar = Perfil.objects.get(id=perfil_id)
	perfil_logado = get_perfil_logado(request)
	
	if(perfil_logado.pode_convidar(perfil_a_convidar)):
		perfil_logado.convidar(perfil_a_convidar)
	
	return  redirect('index')


@login_required
def desfazer(request,perfil_id):
	perfil_logado = get_perfil_logado(request)	
	perfil_logado.desfazer_amizade(perfil_id)

	return  redirect('index')


@login_required
def get_perfil_logado(request):	
	return request.user.perfil


@login_required
def aceitar(request, convite_id):
	convite = Convite.objects.get(id = convite_id)
	convite.aceitar()
	return redirect('index')


@login_required
def recusar(request, convite_id):
	convite = Convite.objects.get(id = convite_id)
	convite.recusar()
	return redirect('index')


@login_required
def redefinir_senha(request):
	perfil_logado = get_perfil_logado(request)
	perfil_logado.redefinir_senha()


@login_required
def setarSuperUsuario(request, perfil_id):
	perfil = Perfil.objects.get(id = perfil_id)
	perfil.usuario.is_superuser = True
	perfil.usuario.save()
	perfil.save()
	
	return redirect('index')


@login_required
def bloquear(request, perfil_id):
	perfil_logado = get_perfil_logado(request)
	perfil_logado.bloquear_contatos(perfil_id)
	return redirect('index')


@login_required
def desbloquear(request, bloqueio_id):
	bloqueio = Bloqueio.objects.get(id = bloqueio_id)
	bloqueio.desbloquear()
	return redirect('index')


@login_required
def deletar_postagem(request, postagem_id):
	postagem = Postagem.objects.get(id=postagem_id)
	postagem.excluir_postagem()

	return redirect('index')





#Conferir as partes de ativar conta

def ativar_conta(request):
	form = AtivarContaForm()
	return render(request, 'ativar_conta.html', {'form':form} )


class AtivarContaView(View):
	def post(self, request):
		form = AtivarContaForm(request.POST)
		if form.is_valid():
			dados_form = form.cleaned_data
			perfil = Perfil.objects.get(nome=dados_form['nome'])
			perfil.usuario.is_active = True
			perfil.usuario.save()
			
			return redirect('index')

		return render(request, 'ativar_conta.html', {'form':form} )



class DesativarContaView(View):
	def get(self, request):
		return render(request, 'desativar_conta.html', {'perfil_logado': get_perfil_logado(request)} )

	def post(self, request):
		form = DesativarContaForm(request.POST)
		if form.is_valid():
			dados_form = form.cleaned_data
			perfil_logado = get_perfil_logado(request)
			perfil_logado.justificativa = dados_form['justificativa']
			perfil_logado.usuario.is_active = False
			perfil_logado.save()
			perfil_logado.usuario.save()
			
			return redirect('index')

		return redirect('index')


class PostarView(View):
	def post(self, request):
		form = PostForm(request.POST)
		if form.is_valid():
			dados_form = form.cleaned_data
			postagem = Postagem()
			postagem.dono = get_perfil_logado(request)
			postagem.texto = dados_form['texto']
			postagem.save()
			return redirect('index')

		return redirect('index')


class PesquisarPerfilView(View):
	def post(self, request):
		form = PesquisaUsuarioForm(request.POST)

		if form.is_valid():
			dados_form = form.cleaned_data
			perfil_logado = get_perfil_logado(request)
			perfis_acessiveis = perfil_logado.pesquisar(dados_form['nome'])
			
			return render(request, 'pesquisa.html', {'perfis': perfis_acessiveis, 'perfil_logado':get_perfil_logado(request)})

		return redirect('index')
