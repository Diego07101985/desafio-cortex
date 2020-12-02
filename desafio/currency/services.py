from datetime import datetime
import requests
import json
from desafio.currency.models import RequestCurrencyQuotationParam


class ServiceQuoteCurrencyPrice(object):
    API_BBC = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    HEADERS = {'accept': 'application/json;odata.metadata=minimal'}

    def _currencies_quote_by_symbol(self, symbol_currency, initial_date, final_date):
        qs = f"?%40moeda='{symbol_currency}'&%40dataInicial='{initial_date}'&%40dataFinalCotacao='{final_date}'&%24format=json"
        api_url_base = f"{self.API_BBC}CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao){qs}"
        try:
            response = requests.get(api_url_base, headers=self.HEADERS)
        except requests.exceptions.ConnectionError:
            return {'error': 'Impossivel estabelecer conecxao'}

        if response.status_code == 200:
            return json.loads(response.content.decode("utf-8"))
        else:
            return None

    def get_all_currencys(self):
        api_url_base = f"{self.API_BBC}Moedas?%24format=json"
        response = requests.get(api_url_base, headers=self.HEADERS)

        if response.status_code == 200:
            result = json.loads(response.content.decode("utf-8"))
            list_currencys = [currency['simbolo']
                              for currency in result['value']]
            return list_currencys
        else:
            return None

    def get_relation_ratio_between_currencies_in_given_period(self, request_params: RequestCurrencyQuotationParam):
        from_currencys = self._currencies_quote_by_symbol(
            request_params.from_simbol, request_params.initial_date,
            request_params.final_date)

        to_currencys = self._currencies_quote_by_symbol(
            request_params.to_simbol, request_params.initial_date,
            request_params.final_date)

        return self._get_value_relation_between_currency(from_currencys, to_currencys,
                                                         [request_params.from_simbol, request_params.to_simbol])

    # Metodo manipula todas as cotacoes de um determinado periodo vindos das chamadas
    # ao endpoint do bbc,  e transforma em  um dicionario com chaves separados pelas datas.
    def _split_currencys_quotation_by_date(self, from_currency, to_currency):
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
    def _get_value_relation_between_currency(self, from_currency, to_currency, currencys):
        quotation_date = self._split_currencys_quotation_by_date(
            from_currency, to_currency)
        currencies_relation_disparity = ''
        list_relation = []
        dict_relation_between = {}
        for key, cotacao in quotation_date.items():
            for i in range(len(quotation_date[key][0])):
                currencies_relation_disparity = quotation_date[key][0][i]['cotacaoCompra'] / \
                    quotation_date[key][1][i]['cotacaoCompra']
                list_relation.append({
                    'relacao_currency': currencies_relation_disparity,
                    'dataHoraCotacao': quotation_date[key][0][i]['dataHoraCotacao'],
                })
                relation_key = currencys[0] + \
                    '-'+currencys[1]+'-'+key

                dict_relation_between.update({relation_key: list_relation})

            list_relation = []

        return dict_relation_between

    def calc_quotes(self, relations_between_currencies, value_currency):
        result_value_convert = []
        for key in relations_between_currencies:
            for relation_calc in relations_between_currencies[key]:
                result_value_convert.append({
                    'valor_convertido': value_currency * relation_calc['relacao_currency'],
                    'dataHoraCotacao': relation_calc['dataHoraCotacao'],
                })

        return result_value_convert
