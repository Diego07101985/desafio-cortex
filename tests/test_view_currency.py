from http import HTTPStatus
from unittest.mock import patch
import desafio.currency.mock_response as mocks


# @patch('desafio.extensions.session_scope')
# def test_1_dever_obter_a_cotacao_da_moeda(self, client):
#     expected_json = mocks.mock_reponse_api
#     url = "/currency?from=GBP&to=JPY&initial_date=11-26-2020&final_date=11-26-2020&amount=1"
#     response = client.get(url)

#     assert response.status_code == HTTPStatus.OK
#     assert response.json.keys() == expected_json.keys()


@patch('desafio.extensions.session_scope')
def test_2_dever_falhar_por_falta_query_string_to_or_from(self, client):
    expected_json = {'error': "required as queries strings from and to"}

    url = "/currency?&to=BRL&initial_date=11-26-2020&final_date=11-26-2020&amount=1"
    response = client.get(url)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == expected_json

    url = "/currency?&from=BRL&initial_date=11-26-2020&final_date=11-26-2020&amount=1"
    response = client.get(url)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == expected_json


@patch('desafio.extensions.session_scope')
def test_3_dever_falhar_por_falta_query_string_to_or_initial_date_or_final_date(self, client):
    expected_json = {'error': "required as queries strings from and to"}

    url = "/currency?from=GBP&to=JPY&final_date=11-26-2020&amount=1"
    response = client.get(url)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == expected_json

    url = "/currency?from=GBP&to=JPY&initial_date=11-26-2020&amount=1"
    response = client.get(url)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == expected_json


@patch('desafio.extensions.session_scope')
def test_4_dever_falhar_ao_buscar_amount_nao_inteiro(self, client):
    expected_key = 'error'
    url = "/currency?&from=BRL&initial_date=11-26-2020&final_date=11-26-2020&amount=error"
    response = client.get(url)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert expected_key in response.json.keys()


# @patch('desafio.extensions.session_scope')
# def test_5_dever_falhar_ao_buscar_moeda_inexistente_na_base(self, client):
#     url = "/currency?from=BTC&to=JPY&initial_date=11-26-2020&final_date=11-26-2020&amount=12"
#     response = client.get(url)
#     assert response.status_code == HTTPStatus.NO_CONTENT


# @patch('desafio.extensions.session_scope')
# def test_6_dever_retornar_miss_na_hit_na_resposta(self, client):
#     expected_json = {
#         "status": "MISS",
#         "results": []
#     }
#     url = "/currency?from=GBP&to=JPY&initial_date=11-26-2020&final_date=11-26-2020&amount=1"
#     response = client.get(url)
#     assert response.status_code == HTTPStatus.OK
#     assert response.json['status'] == expected_json['status']
