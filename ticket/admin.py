from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'status', 'descricao', 'horario_inicial_atendimento', 'horario_final_atendimento', 'sla')
    list_filter = ('status', 'horario_inicial_atendimento', 'setor', 'horario_final_atendimento')
    search_fields = ('nome', 'descricao', 'setor')

    fieldsets = (
        (None, {'fields': ('nome', 'email', 'setor', 'categoria', 'descricao', 'patrimonio')}),
        ('Status e Tempo', {'fields': ('status', 'horario_inicial_atendimento', 'pausa_horario_atendimento', 'horario_retomado_atendimento', 'horario_final_atendimento')}),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            # O objeto está sendo criado, então apenas salve-o sem calcular SLA
            super().save_model(request, obj, form, change)
            return

        # O objeto já existe, podemos calcular o SLA
        if obj and obj.calcular_sla(obj.status):
            super().save_model(request, obj, form, change)

    def save_form(self, request, form, change):
        obj = super().save_form(request, form, change)
        if obj.calcular_sla(obj.status):
            return obj
        return None