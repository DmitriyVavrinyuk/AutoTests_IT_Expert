import json
from my_lib.assertions import Assertion
import warnings
from my_lib.my_requests import MyRequests
from my_lib.base_case import BaseCase
import allure


# Название: Актуализация атрибутов и статусов ОС
# Место положение: раздел ИТА
# Тест кейс:
# Описание: https://cf.itexpert.ru/pages/viewpage.action?pageId=155487983

# python -m pytest -s test_update_os_directory.py -k TestUpdateUnit
# python -m pytest -s tests\test_update_unit.py -k TestUpdateUnit
# python -m pytest --alluredir=allure_result_folder tests/test_update_unit.py

# Интеграционное взаимодействие - Импорт единиц измерения из ЕСМ. Запрос создает запись в спраовчнике "Единицы измерения".
@allure.epic("Интеграционное взаимодействие - Импорт единиц измерения из ЕСМ. Запрос создает запись в спраовчнике 'Единицы измерения'.")
class TestUpdateUnit(BaseCase):
# Авторизация и получение необходимых cookie и headers
    @allure.description("Авторизация и получение необходимых cookie и headers")
    def setup(self):
        env = 'http://localmail.itexpert.ru:5055'
        auth_data = {
            "UserName": "Supervisor",
            "UserPassword": "!Supervisor123Test!"
        }

        self.url = "http://localmail.itexpert.ru:5055/rest/IteESMIntegrationService/v1/UpdateOSDirectory"
        self.jar, self.header = MyRequests.user_auth(self, auth_data, env)

    # python -m pytest -s test_update_unit.py -k TestUpdateUnit - k test_request_for_supply
    #

    @allure.description("тест")
    def test_request_for_supply(self):
        json_data = {

                "currentPage": 1,
                "pageCount": 1,
                "delta": "F",
                "item": [
                    {
                        "ANLN1": "240000240179",
                        "TXT50": "Аппарат телефонный Cisco/CP-7945G=13",
                        "INVNR": "12121313",
                        "SERNR": "qwerty13",
                        "AKTIV": "30.03.2016",
                        "KOSTL": "123",
                        "WERKS": "1001",
                        "STORT": "43",
                        "ANSW_END": "20000.00",
                        "RBW_END": "10000",
                        "MENGE": "1",
                        "POSNR": "1100648.80016-YO04-00013",
                        "GLO_RUS_OKOF16": "330.28.12",
                        "GLO_RUS_DEPGRN": "03",
                        "NDJAR": "004",
                        "DEAKT": "13.02.2023",
                        "KTEXT3": "г.Санкт-Петербург ул.Почтамтская 3-5",
                        "ZZCNDPERNR": "00028076",
                        "CNDPERNR_NAME": "Дернов ИН123",
                        "OS_STATUS": "Перемещен",
                        "AWKEY": "09072021/2",
                        "GJAHR": "2021",
                        "ACT-ID": "pre09072021/2",
                        "row": 1,
                        "deleted": ""
                    }
                ]
            }

        # Проверка обязательных полей
        # json_data_dict = json_data["UOM"]
        # assert json_data_dict["Code"] != "", "Параметр Code не может быть пустым."
        # assert json_data_dict["Name"] != "", "Параметр Name не может быть пустым."
        #
        response = MyRequests.post(self.url, json=json_data, headers=self.header, cookies=self.jar)
        Assertion.assert_code_status(response, 200)
        print(response.text)
        obj = json.loads(response.text)
        # print(obj)
        # for result, value in obj.items():
        #     # print(result, value)
        #     assert obj["message"] == None, f"The value of 'MESSAGE' is not correct"
        #     assert obj['success'] == True, f"The value of 'TYPE' is not correct"