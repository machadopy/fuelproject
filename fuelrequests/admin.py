from django.contrib import admin
from .models import Fuelrequests
from django.utils.html import format_html


@admin.register(Fuelrequests)
class FuelrequestsAdmin(admin.ModelAdmin):


    list_display = [
        'id',
        'usuario', 
        'veiculo', 
        'data_solicitacao', 
        'km_inicial', 
        'km_final', 
        'get_distancia', 
        'status',
        'hodometro_preview',
    ]
    list_display_links = [
        'id',
        'usuario', 
        'veiculo', 
        'data_solicitacao',
        ]
    
    search_fields = [
        'id',
        'usuario', 
        'veiculo', 
        'data_solicitacao', 
        'km_inicial', 
        'km_final', 
        'get_distancia', 
        'status',
        'hodometro_preview'
    ]

    list_editable = ['status']
    
    list_filter = ('status', 'data_solicitacao', 'veiculo', 'usuario')
    
    
    readonly_fields = ('data_solicitacao','hodometro_preview')


    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'veiculo', 'status',)
        }),
        ('Controle de Quilometragem', {
            'fields': ('km_inicial', 'km_final')
        }),
        ('Datas', {
            'fields': ('data_solicitacao',),
        }),
        ('Comprovante', {
        'fields': ('hodometro','hodometro_preview')
        }),
    )
    list_per_page = 10






    # Função auxiliar para conseguir exibir sua @property 'distancia_percorrida' como coluna na tabela
    @admin.display(description='Distância Percorrida')
    def get_distancia(self, obj):
        return obj.distancia_percorrida

    @admin.display(description='Preview')
    def hodometro_preview(self, obj):
        if obj.hodometro:
            return format_html(
                '<img src="{}" style="max-height: 80px; max-width: 120px; border-radius: 4px;" />',
                obj.hodometro.url
            )
        return '(sem imagem)'

 