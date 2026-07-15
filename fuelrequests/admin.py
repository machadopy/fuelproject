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
    
    # 2. Filtros rápidos na lateral direita do painel
    list_filter = ('status', 'data_solicitacao', 'veiculo', 'usuario')
    
    # 3. Barra de busca (pesquisa pelo nome do usuário ou placa do veículo)
    search_fields = ('usuario__username', 'veiculo__placa', 'status')
    
    # 4. Define quais campos são apenas para leitura (não podem ser editados manualmente no admin)
    readonly_fields = ('data_solicitacao',)

    # 5. Organiza como os campos aparecem ao clicar para editar uma solicitação
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'veiculo', 'status')
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