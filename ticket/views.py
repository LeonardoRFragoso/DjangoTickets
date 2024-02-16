from django.shortcuts import render, redirect
from .models import Ticket

def home(request):
    return render(request, "ticket/home.html")

def obg(request):
    return render(request, "ticket/obg.html")

def submit(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        setor = request.POST.get('setor')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        patrimonio = request.POST.get('patrimonio')
        status = 'AguardandoAtendimento'

        novo_ticket = Ticket.objects.create(
            nome=nome,
            email=email,
            setor=setor,
            categoria=categoria,
            descricao=descricao,
            patrimonio=patrimonio,
            status=status
        )

        return redirect('obg')

    return render(request, 'ticket/home.html')

def lista_tickets(request):
    tickets = Ticket.objects.all()
    return render(request, 'ticket/admin/card.html', {'tickets': tickets})
