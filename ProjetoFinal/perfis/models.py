from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class Perfil(models.Model):
#     nome = models.CharField(max_length=255, null=False)
#     telefone = models.CharField(max_length=20, null= False)
#     nome_empresa = models.CharField(max_length=255, null=False)
#     email = models.CharField(max_length=255, null=False)
#     contatos = models.ManyToManyField('Perfil')

class Perfil(models.Model):
    nome = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=15, null=False)
    nome_empresa = models.CharField(max_length=255, null=False)
    contatos = models.ManyToManyField('self', related_name = 'meus_contatos')
    contatos_bloqueados = models.ManyToManyField('self', related_name = 'meus_contatos_bloqueados', symmetrical=False, through='Bloqueio')
    usuario = models.OneToOneField(User, related_name="perfil", on_delete = models.CASCADE)
    foto_perfil = models.ImageField(upload_to='fotos_perfis', null=True, blank = True)
    
    
    @property
    def email(self):
        return self.usuario.email

    @property
    def superuser(self):
        return self.usuario.is_superuser
    
    @property
    def meus_bloqueios(self):
        bloqueio = Bloqueio.objects.filter(bloqueador=self)
        return bloqueio

    def bloqueados(self):
        lista_bloqueados = []
        for i in self.meus_bloqueios:
            lista_bloqueados.append(i.bloqueado)

        return lista_bloqueados
    
    def contatos_nao_bloqueados(self):

        perfis_nao_bloqueados = []
        perfis_me_bloquearam = Bloqueio.objects.filter(bloqueado=self)
        ids_perfis_me_bloquearam = []
        
        for perfil in perfis_me_bloquearam:
            ids_perfis_me_bloquearam.append(perfil.bloqueador.id)
       
        for i in Perfil.objects.all():
            if i.id not in ids_perfis_me_bloquearam and i not in self.meus_bloqueios.all():
                perfis_nao_bloqueados.append(i)
        
        return perfis_nao_bloqueados

    def contatos_me_bloquearam(self):
        perfis_me_bloquearam = Bloqueio.objects.filter(bloqueado=self)
        ids_perfis_me_bloquearam = []
        for i in perfis_me_bloquearam:
            ids_perfis_me_bloquearam.append(i.bloqueador.id)

        return ids_perfis_me_bloquearam


    def pesquisar(self, nome_perfil):
        resultado_pesquisa = []
        perfis = Perfil.objects.filter(nome__icontains=nome_perfil)
        ids_perfis_me_bloquearam = self.contatos_me_bloquearam()

        for perfil in perfis:
            if perfil.id not in ids_perfis_me_bloquearam and perfil.id != self.id:
                resultado_pesquisa.append(perfil)

        return resultado_pesquisa

    @property
    def get_postagens(self):
        return Postagem.objects.filter(id=self.id)
            

    def __str__(self):
        return self.nome

    def desfazer_amizade(self, perfil_id):
        self.contatos.remove(perfil_id)
        

    def convidar(self, perfil_convidado):
        if self.pode_convidar(perfil_convidado):
            convite = Convite(solicitante=self,convidado = perfil_convidado)
            convite.save()  

    def pode_convidar(self, perfil):    
        convites = Convite.objects.filter(solicitante=self, convidado=perfil).all()
        if len(convites) == 0:
            return self.id != perfil.id and perfil not in self.contatos.all()
        
        return False

    def pode_bloquear(self, perfil):
        for i in self.meus_bloqueios.all():
            if i.bloqueado.id == perfil.id:
                return False    
        return self.id != perfil.id

    def pode_exibir(self, perfil):
        for i in perfil.meus_bloqueios.all():
            if i.bloqueado.id == self.id:
                return False    
        return True
            


    def bloquear_contatos(self, perfil_id):
        perfil = Perfil.objects.get(id=perfil_id)
        bloqueio = Bloqueio()
        bloqueio.bloqueador = self
        bloqueio.bloqueado = perfil
        bloqueio.save()


class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil,on_delete=models.CASCADE,related_name='convites_feitos' )
    convidado = models.ForeignKey(Perfil, on_delete= models.CASCADE, related_name='convites_recebidos')

    def aceitar(self):        
        self.solicitante.contatos.add(self.convidado)
        self.convidado.contatos.add(self.solicitante)
        self.delete()

    def recusar(self):
        self.delete()


class Postagem(models.Model):
    dono = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='minhas_postagens')

    texto = models.CharField(max_length=400, null=False)
    data_publicacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.texto

    def excluir_postagem(self):
        self.delete()


class Bloqueio(models.Model):
    bloqueador = models.ForeignKey(Perfil, on_delete = models.CASCADE, related_name = 'bloqueador')
    bloqueado = models.ForeignKey(Perfil, on_delete = models.CASCADE, related_name = 'bloqueado')

    def __str__(self):
        return self.bloqueado.nome

    def desbloquear(self):
        self.delete()