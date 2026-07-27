from django.contrib import admin
from .models import Fuelrequests


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
    ]

    list_editable = ['status']
    
    list_filter = ('status', 'data_solicitacao', 'veiculo', 'usuario')
    
    search_fields = ('usuario__username', 'veiculo__placa', 'status')
    
    readonly_fields = ('data_solicitacao',)

    filter_horizontal = ('tags',)


    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'veiculo', 'status','tags',)
        }),
        ('Controle de Quilometragem', {
            'fields': ('km_inicial', 'km_final')
        }),
        ('Datas', {
            'fields': ('data_solicitacao',),
        }),
    )
    list_per_page = 10






    # Função auxiliar para conseguir exibir sua @property 'distancia_percorrida' como coluna na tabela
    @admin.display(description='Distância Percorrida')
    def get_distancia(self, obj):
        return obj.distancia_percorrida

    @admin.display(description='Tags')
    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

 