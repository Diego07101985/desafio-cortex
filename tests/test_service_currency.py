import json
from unittest.mock import Mock
from unittest.mock import patch
from desafio.currency.services import ServiceQuoteCurrencyPrice
import desafio.currency.mock_response as mocks
import unittest


class TestServiceQuoteCurrencyPrice(unittest.TestCase):

    def setUp(self):
        self.service_currence = ServiceQuoteCurrencyPrice()

    def _mock_response(
            self,
            status=200,
            json_data=None,
            raise_for_status=None):

        mock_resp = Mock()
        mock_resp.raise_for_status = Mock()

        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status

        mock_resp.status_code = status

        if json_data:
            mock_resp.content = Mock()
            mock_resp.content.decode = Mock()
            mock_resp.content.decode.return_value = json.dumps(json_data)

        return mock_resp

    @patch('requests.get')
    def test_1_deve_retornar_none_retornar_currencys_bcb(self, mock_get):
        mock_resp = self._mock_response(
            json_data=mocks.mock_response_endpoint_bcb)
        mock_get.return_value = mock_resp

        currencys = self.service_currence.get_all_currencys()
        self.assertTrue('AUD' in currencys)
        self.assertTrue('CAD' in currencys)
        self.assertTrue('CHF' in currencys)

    @patch('requests.get')
    def test_2_deve_retornar_a_cotacao_da_moeda(self, mock_get):
        self.relations_between_currencies = {'GBP-JPY-11-26-2020-11-26-2020': [
            {'relacao_currency': 139.233,
             'dataHoraCotacao': '2020-11-26 10:11:18.759'}
        ]}
        return_calc = self.service_currence.calc_quotes(
            self.relations_between_currencies, 10)
        self.assertEqual(return_calc[0]['valor_convertido'], 1392.33)
