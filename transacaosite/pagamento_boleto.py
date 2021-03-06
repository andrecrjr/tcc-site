import pagarme, isodate
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from transacaosite.models import *
from apisite.models import Inventario
import json

pagarme.authentication_key(settings.PAGAR_ME_TOKEN)


def calc_moeda(trans):
    valor_total = 0
    for dados in trans:
        preco_com_quantidade = float(dados['preco_item']) * int(dados['quantidade'])
        valor_total += preco_com_quantidade
    valor_total = valor_total * 100
    valor_total = int(valor_total)
    return str(valor_total)


def calc_total(trans):
    valor_total = 0
    for dados in trans:
        preco_com_quantidade = float(dados['preco_item']) * int(dados['quantidade'])
        valor_total += preco_com_quantidade
    return str(valor_total)


def params_boleto(valor_total, email_usuario, nome_usuario):
    params = {
        'amount': valor_total,
        'payment_method': 'boleto',
        'customer': {
            'type': 'individual',
            'country': 'br',
            'email': email_usuario,
            'name': nome_usuario,
            'documents': [
                {
                    'type': 'cpf',
                    'number': '00000000000'
                }
            ]
        }
    }
    return params


def request_boleto(request):
    if request.method == 'GET':
        usuario = Inventario.objects.get(id=request.user.pk)
        itens = request.session.get('boleto_' + request.user.username)
        valor_moeda = calc_moeda(itens)
        if 1.0 > float(calc_total(itens)):
            itens.clear()
            return render(request, 'marketplace.html', {'error': 'O boleto tem que valer maior que R$1'})
        else:
            try:
                params = params_boleto(valor_moeda, request.user.email, request.user.first_name)
                transact = pagarme.transaction.create(params)
                time_expiration = convert_data_to_datetime(transact)
                Transacao.objects.create(usuario_transacao=usuario,
                                                        status_boleto=False,
                                                        codigo_boleto=transact['tid'],
                                                        expiration_boleto_date = time_expiration,
                                                        valor_boleto = calc_total(itens)
                                                        )
                request.session['codigo_boleto'] = transact['tid']
                ItemSession.objects.create(user=Inventario.objects.get(usuario=request.user.pk),
                                                            itens=json.dumps(itens), codigo_boleto=transact['tid'])
                return redirect('/marketplace/boleto/')
            except:
                return render(request, 'marketplace.html', {'error': 'Servidor fora do ar ou sem conexão com internet'})



def convert_data_to_datetime(trans):
    data_boleto = trans['boleto_expiration_date']
    data = isodate.parse_datetime(data_boleto)
    return data


def get_data_from_boleto(request):
    if request.method == 'GET':
        try:
            codigo = request.session.get('codigo_boleto', [])
            json = pagarme.transaction.find_by({"id":str(codigo)})
            return JsonResponse(json, safe=False, status=200)
        except:
            return JsonResponse({'error':'nothing found'}, status=404)


def paid_boleto(request):
    if request.method == 'GET':
        codigo = request.session.get('codigo_boleto')
        itens = request.session.get('boleto_' + request.user.username)
        if not itens:
            itens_db = items_from_session(request.user.pk)
            json_itens = json.loads(itens_db.itens)
            itens = json_itens
            if not codigo:
                codigo = itens_db.codigo_boleto
        if itens and codigo and pay_boleto_pagarme(codigo):
            trans = Transacao.objects.get(codigo_boleto=codigo)
            for dados in itens:
                item = Item.objects.get(id_item=int(dados['id_item']))
                pedido = ItemCompra.objects.create(item=item,
                                                   item_transacao=trans,
                                                   quantidade=dados['quantidade'])
                inventario_salvo = verify_itens_in_inventario(item,request.user.pk, int(dados['quantidade']))
                pedido.save()
            trans.status_boleto = True
            trans.save() 
            itens.clear()
            del codigo
            request.session.modified = True
        return redirect('/marketplace/')

def verify_itens_in_inventario(item, id_usuario, quantidade_item):
    usuario = Inventario.objects.get(usuario=id_usuario)
    try:
        itens_usuario = InventarioItemGame.objects.filter(usuario=usuario, item=item)
        if itens_usuario:
            for id, item in enumerate(itens_usuario):
                inventario = InventarioItemGame.objects.get(id=itens_usuario[id].id)
                inventario.quantidade += int(quantidade_item)
                return inventario.save()
        inventario_game = InventarioItemGame.objects.create(usuario=usuario, item=item, quantidade=quantidade_item)
        return inventario_game.save()
    except:
        itens_usuario = InventarioItemGame.objects.create(usuario=usuario,
                                                        item=item, quantidade=quantidade_item)
        return itens_usuario.save()

def items_from_session(user):
    inventario = Inventario.objects.get(usuario=user)
    item_salvo = ItemSession.objects.filter(user=inventario).order_by('-id')[0]
    return item_salvo

def pay_boleto_pagarme(id_boleto):
    try:
        pagarme.transaction.pay_boleto(id_boleto, {'status': 'paid'})
        return True
    except:
        return False