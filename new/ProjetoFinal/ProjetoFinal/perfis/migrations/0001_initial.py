# Generated by Django 2.1.5 on 2019-01-17 23:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bloqueio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Convite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('telefone', models.CharField(max_length=15)),
                ('nome_empresa', models.CharField(max_length=255)),
                ('contatos', models.ManyToManyField(related_name='_perfil_contatos_+', to='perfis.Perfil')),
                ('contatos_bloqueados', models.ManyToManyField(related_name='meus_contatos_bloqueados', through='perfis.Bloqueio', to='perfis.Perfil')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Postagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=400)),
                ('data_publicacao', models.DateTimeField(auto_now_add=True)),
                ('dono', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='minhas_postagens', to='perfis.Perfil')),
            ],
        ),
        migrations.AddField(
            model_name='convite',
            name='convidado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convites_recebidos', to='perfis.Perfil'),
        ),
        migrations.AddField(
            model_name='convite',
            name='solicitante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convites_feitos', to='perfis.Perfil'),
        ),
        migrations.AddField(
            model_name='bloqueio',
            name='bloqueado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bloqueado', to='perfis.Perfil'),
        ),
        migrations.AddField(
            model_name='bloqueio',
            name='bloqueador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bloqueador', to='perfis.Perfil'),
        ),
    ]
