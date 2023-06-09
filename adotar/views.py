from django.shortcuts import render, redirect
from divulgar.models import Pet, Raca
from django.contrib.messages import constants
from django.contrib import messages
from.models import PedidoAdocao
from datetime import datetime
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your views here.

def listar_pets(request):
    if request.method == "GET":
        pets = Pet.objects.filter(status='P')
        racas = Raca.objects.all()
        
        cidade = request.GET.get('cidade')
        raca_filter = request.get.get('raca')

        if cidade:
            pets == pets.filter(cidade__icontains=cidade)

        if raca_filter:
            pets = pets.filter(raca__id=raca_filter) 
            raca_filter = Raca.objects.get(id=raca_filter)   

        return render(request, 'listar_pets.html', {'pets': pets, 'racas': racas, 'cidade': cidade, 'raca_filter': raca_filter})

def pedido_adocao(request, id_pet):
    pet = Pet.objects.filter(id=id_pet) .filter(status="P")

    if not pet.exists():
        messages.add_message(request, constants.WARNING, 'Esse pet ja foi adotado')

    pedido = PedidoAdocao(pet=pet.first(),
                          usuario=request.user,
                          data=datetime.now())  
    
    pedido.save()
    messages.add_message(request, constants.SUCCESS, 'Esse pedido de adoção foi um sucesso')


    return redirect('/adotar')

def processa_pedido_adocao(request, id_pedido):
    status = request.GET.get('status')
    pedido = PedidoAdocao.objects.get(id=id_pedido)

    if status == "A":
        pedido.status = 'AP'
        string= '''Ola sua adoção foi aprovada com sucesso'''
    elif status == "R":
        string= '''Ola sua adoção foi recusada'''
        pedido.status = "R"    

    pedido.save() 

    email = send_mail(
            'Sua adoção foi processada',
        string,  
            'gonsalves87@hotmail.com'
            [pedido.usuario.email,]
        )
    messages.add_message(request, constants.SUCCESS, 'Pedido de adoção processado')
    return redirect('/divulgar/ver_pedido_adocao')

    return HttpResponse(status)
    