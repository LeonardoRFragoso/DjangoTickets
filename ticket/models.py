from django.db import models
from django.utils import timezone
from datetime import timedelta

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('AguardandoAtendimento', 'Aguardando Atendimento'),
        ('EmAndamento', 'Em Andamento'),
        ('Pendente', 'Pendente'),
        ('Concluido', 'Concluído'),
    ]

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False)
    setor = models.CharField(max_length=255, null=False, blank=False)
    categoria = models.CharField(max_length=255, null=False, blank=False)
    descricao = models.CharField(max_length=255, null=False, blank=False)
    patrimonio = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='AguardandoAtendimento')
    horario_inicial_atendimento = models.DateTimeField(null=True, blank=True)
    horario_final_atendimento = models.DateTimeField(null=True, blank=True)
    pausa_horario_atendimento = models.DateTimeField(null=True, blank=True)
    horario_retomado_atendimento = models.DateTimeField(null=True, blank=True)
    sla = models.DurationField(null=True, blank=True)

    def calcular_sla(self, new_status):
        if self:
            now = timezone.now()
        if self and hasattr(self, '_meta') and self._meta:
            cleaned_old_status = ''.join(e for e in self.status.lower() if e.isalnum())
            cleaned_new_status = ''.join(e for e in new_status.lower() if e.isalnum())

            if cleaned_old_status != cleaned_new_status:
                if cleaned_old_status == 'aguardandoatendimento' and cleaned_new_status == 'emandamento':
                    self.horario_inicial_atendimento = now
                elif cleaned_old_status == 'emandamento' and cleaned_new_status == 'pendente':
                    self.pausa_horario_atendimento = now
                elif cleaned_old_status == 'pendente' and cleaned_new_status == 'emandamento':
                    if self.horario_retomado_atendimento:
                        self.horario_retomado_atendimento += now - self.pausa_horario_atendimento
                    else:
                        self.horario_retomado_atendimento = now - self.pausa_horario_atendimento

                self.status = new_status

                if cleaned_new_status == 'concluido':
                    self.horario_final_atendimento = now
                    tempo_total = self.horario_final_atendimento - self.horario_inicial_atendimento
                    tempo_pausado = self.horario_retomado_atendimento - self.pausa_horario_atendimento if self.horario_retomado_atendimento else timedelta()

                    sla = (tempo_total - tempo_pausado).total_seconds() / 3600  # convertendo segundos para horas

                    self.sla = sla
                else:
                    self.sla = None  # Se não estiver concluído, SLA é nulo

                self.save()  # Salvando o valor calculado ou nulo no banco de dados

                return True  # Retorne True se a função foi bem-sucedida

            return False  # Retorne False se o status não mudar
