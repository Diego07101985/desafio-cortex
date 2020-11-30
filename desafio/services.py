import json
import requests


class ServiceQuoteCurrencyPrice(object):
    API_BBC = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    HEADERS = {'accept': 'application/json;odata.metadata=minimal'}

    def get_currencies_quote(self, symbol_currency, initial_date, final_date):
        qs = f"?%40moeda={symbol_currency}&%40dataInicial={initial_date}&%40dataFinalCotacao={final_date}&%24format=json"
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
            return json.loads(response.content.decode("utf-8"))
        else:
            return None
