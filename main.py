import json
from my_lib.assertions import Assertion
from my_lib.my_requests import MyRequests
from my_lib.base_case import BaseCase

# python -m pytest -s main.py -k TestAuth
# Тестирование авторизации "Замена позиций в запросе на закупку"

class TestAuth(BaseCase):

    # Авторизация и получение необходимых cookie и headers

    def setup(self):
        env = 'http://localmail.itexpert.ru:5057'
        auth_data = {
            "UserName": "Supervisor",
            "UserPassword": "!Supervisor123Test!"
        }

        self.url = "http://localmail.itexpert.ru:5057/rest/SapErpIntegrationService/v1/UpdateRequestUB"
        self.jar, self.header = MyRequests.user_auth(self, auth_data, env)

    def test1(self):
        json_data = {
            "currentPage": "1",
            "pageCount": "1",
            "delta": "F",
            "item": [
                {
                    "row": "1",
                    "BANFN_IT": "RP00000030",       # Номер потребности в СУИТА
                    "BNFPO_IT": "2",        # Позиция потребности в СУИТА
                    "BANFN": "0010017683",      # Номер корректируемой заявки подразделения (вида UB)
                    "BNFPO": "00020",           # Номер позиции корректируемой заявки подразделения (вида UB)
                    # "BANFN": "0010017683",    # Номер корректирующей заявки подразделения (вида UB)
                    "ZZ_BNFPO": "00010",        # Номер позиции корректирующей заявки подразделения (вида UB)
                    "PS_PSP_PNR": "010001.000.RE-33-0000-01",  # Код СПП-элемента
                    "MATNR": "770000023154",    # № материала в SAP
                    "MENGE": "90.0",            # Количество материала
                    "MEINS": "ШТ",              # Единица измерения
                    "ZZ_KLASS": "",             # Класс оценки
                    "FISTL": "100117000",       # ПФМ
                    "GEBER": "NOPROJECT",       # Фонд
                    "FIPOS": "6070101",         # Финансовая позиция
                    "PREIS": "47000.00",        # Плановая цена
                    "ZEBKN": "48000.00",        # Вид контировки
                    "AUFNR": "49000.00",        # Заказ
                    "KOSTL": "45000.00",        # МВЗ
                    "ANLN1": "Q",               # Основное средство
                    "KNTTP": "Q",               # Номер потребности в СУИТА
                    "deleted": ""               # Номер потребности в СУИТА
                }
            ]
        }
        response = MyRequests.post(self.url, json=json_data, headers=self.header, cookies=self.jar)
        Assertion.assert_code_status(response, 200)
        print(response.text)
        obj = json.loads(response.text)
        print(obj)

        # for result in obj['result']:
        #     print(result['TYPE'])
        #     assert result['TYPE'] == "S", f"The value of 'TYPE' is not correct"
        #     assert result['MESSAGE'] == "", f"The value of 'MESSAGE' is not correct"


