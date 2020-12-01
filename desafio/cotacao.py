from datetime import datetime
from datetime import timedelta

iene = {
    "simbolo": "JPY",
    "nomeFormatado": "Iene",
    "tipoMoeda": "A"
}

gbp = {
    "simbolo": "GBP",
    "nomeFormatado": "Libra Esterlina",
    "tipoMoeda": "B"
}

currencys = [gbp, iene]

result_gbp = {"value": [
    {
        "paridadeCompra": 1.3346,
        "paridadeVenda": 1.335,
        "cotacaoCompra": 7.1165,
        "cotacaoVenda": 7.1194,
        "dataHoraCotacao": "2020-11-26 10:11:18.759",
        "tipoBoletim": "Abertura"
    }, {
        "paridadeCompra": 1.3346,
        "paridadeVenda": 1.335,
        "cotacaoCompra": 7.1165,
        "cotacaoVenda": 7.1194,
        "dataHoraCotacao": "2020-11-26 10:11:18.754",
        "tipoBoletim": "Abertura"
    }, {
        "paridadeCompra": 1.3334,
        "paridadeVenda": 1.3338,
        "cotacaoCompra": 7.0978,
        "cotacaoVenda": 7.1008,
        "dataHoraCotacao": "2020-11-27 11:11:18.775",
        "tipoBoletim": "Intermediário"
    }]}

result_jpy = {"value": [

    {
        "paridadeCompra": 104.25,
        "paridadeVenda": 104.26,
        "cotacaoCompra": 0.05114,
        "cotacaoVenda": 0.05115,
        "dataHoraCotacao": "2020-11-26 10:11:18.759",
        "tipoBoletim": "Abertura"
    },
    {
        "paridadeCompra": 104.25,
        "paridadeVenda": 104.26,
        "cotacaoCompra": 0.05114,
        "cotacaoVenda": 0.05115,
        "dataHoraCotacao": "2020-11-26 10:11:18.754",
        "tipoBoletim": "Abertura"
    },
    {
        "paridadeCompra": 104.24,
        "paridadeVenda": 104.27,
        "cotacaoCompra": 0.05105,
        "cotacaoVenda": 0.05107,
        "dataHoraCotacao": "2020-11-27 11:11:18.775",
        "tipoBoletim": "Intermediário"
    }

]}


# Metodo manipula todas as cotacoes de um determinado periodo vindos das chamadas
# ao endpoint do bbc,  e transforma em  um dicionario com chaves separados pelas datas.
def split_currencys_quotation_by_date(from_currency, to_currency):
    relation_date = None
    previous_date_relation = None
    date_dict = {}
    list_date_key = []
    list_from_quotation = []
    list_to_quotation = []

    for i in range(len(from_currency['value'])):
        parser_date = datetime.strptime(
            from_currency['value'][i]['dataHoraCotacao'], '%Y-%m-%d %H:%M:%S.%f')
        relation_date = datetime.strptime(
            parser_date.strftime('%Y-%m-%d'), '%Y-%m-%d')
        key = relation_date.strftime(
            '%Y-%m-%d')
        if key not in list_date_key:
            list_date_key.append(key)

    for i in range(len(from_currency['value'])):
        parser_date = datetime.strptime(
            from_currency['value'][i]['dataHoraCotacao'], '%Y-%m-%d %H:%M:%S.%f')
        date_key = datetime.strptime(
            parser_date.strftime('%Y-%m-%d'), '%Y-%m-%d')

        if not previous_date_relation:
            previous_date_relation = date_key.strftime('%Y-%m-%d')

        if previous_date_relation != date_key.strftime('%Y-%m-%d'):
            list_from_quotation = []
            list_to_quotation = []
            previous_date_relation = date_key.strftime('%Y-%m-%d')
            date_dict[key] = [list_from_quotation, list_to_quotation]

        if date_key.strftime('%Y-%m-%d') in list_date_key:
            list_from_quotation.append(from_currency['value'][i])
            list_to_quotation.append(to_currency['value'][i])
            date_dict.update(
                {date_key.strftime('%Y-%m-%d'): [list_from_quotation, list_to_quotation]})
    return date_dict


# Neste metodo é obtido o calculo para obtencao da resultante da disparidade
# entre as duas moedas frente ao real.
def get_relation_between_currency(from_currency, to_currency, currencys):
    quotation_date = split_currencys_quotation_by_date(
        from_currency, to_currency)
    currencies_relation_disparity = ''
    lista_relacao = []
    dict_relation_between = {}
    for key, cotacao in quotation_date.items():
        for i in range(len(quotation_date[key][0])):
            currencies_relation_disparity = quotation_date[key][0][i]['cotacaoCompra'] / \
                quotation_date[key][1][i]['cotacaoCompra']
            lista_relacao.append({
                'relacao_currency': currencies_relation_disparity,
                'dataHoraCotacao': quotation_date[key][0][i]['dataHoraCotacao'],
            })
            relation_key = currencys[0] + \
                '-'+currencys[1]+'-'+key

            dict_relation_between.update({relation_key: lista_relacao})

        lista_relacao = []

    return dict_relation_between
