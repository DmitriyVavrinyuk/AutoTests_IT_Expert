import json
from my_lib.assertions import Assertion
import warnings
from my_lib.my_requests import MyRequests
from my_lib.base_case import BaseCase
import allure


# Название: Импорт единиц измерения из ЕСМ
# Место положение: Cпраовчник "Единицы измерения"
# Тест кейс: https://jira.itexpert.ru/secure/Tests.jspa#/testCase/IT4ITMVP-T2107
# Описание: https://cf.itexpert.ru/pages/viewpage.action?pageId=167085306

# python -m pytest -s test_update_unit.py -k TestUpdateUnit
# python -m pytest -s tests\test_update_unit.py -k TestUpdateUnit
# python -m pytest --alluredir=allure_result_folder tests/test_update_unit.py

# Интеграционное взаимодействие - Импорт единиц измерения из ЕСМ. Запрос создает запись в спраовчнике "Единицы измерения".
@allure.epic("Интеграционное взаимодействие - Импорт единиц измерения из ЕСМ. Запрос создает запись в спраовчнике 'Единицы измерения'.")
class TestUpdateUnit(BaseCase):
# Авторизация и получение необходимых cookie и headers
    @allure.description("Авторизация и получение необходимых cookie и headers")
    def setup(self):
        env = 'http://localmail.itexpert.ru:5057'
        auth_data = {
            "UserName": "Supervisor",
            "UserPassword": "!Supervisor123Test!"
        }

        self.url = "http://localmail.itexpert.ru:5057/rest/IteESMIntegrationService/v1/UpdateUnit"
        self.jar, self.header = MyRequests.user_auth(self, auth_data, env)

    # python -m pytest -s test_update_unit.py -k TestUpdateUnit - k test_request_for_supply
    #

# Запрос создает запись в спраовчнике "Единицы измерения"
# Поиск значений в справочнике осуществляется по Поле Код КСУ НСИ "Code"
# Если значение найдено - обновляем атрибуты, если не найдено - Импортируются данные по единицам измерения и справочник ИТ-активов..
# Если "Deletion_mark": "True" то запись с соответсвующем Код КСУ НСИ буде удалена
    @allure.description("Запрос создает запись в спраовчнике 'Единицы измерения'"
                        "Поиск значений в справочнике осуществляется по Поле Код КСУ НСИ 'Code' "
                        "Если значение найдено - обновляем атрибуты, "
                        "Если не найдено - Импортируются данные по единицам измерения в справочник ИТ-активов. "
                        "Если 'Deletion_mark': 'True' то запись с соответсвующем Код КСУ НСИ буде удалена")
    def test_request_for_supply(self):
        json_data = {
                        "UOM":
                            { #Справочник единицы измерения
                                "Code": "072",          #Поле Код КСУ НСИ
                                "Name": "КГ2",          #Поле Название
                                "Code_ISO": "KGM",
                                "Code_SAPERP60": "KG",
                                "Code_OKEI": "166",
                                "Deletion_mark": True  #Пометка на удаление (Деактивация)
                            }
                        }

        # Проверка обязательных полей
        json_data_dict = json_data["UOM"]
        assert json_data_dict["Code"] != "", "Параметр Code не может быть пустым."
        assert json_data_dict["Name"] != "", "Параметр Name не может быть пустым."

        response = MyRequests.post(self.url, json=json_data, headers=self.header, cookies=self.jar)
        Assertion.assert_code_status(response, 200)
        # print(response.text)
        obj = json.loads(response.text)
        print(obj)
        for result, value in obj.items():
            # print(result, value)
            assert obj["message"] == None, f"The value of 'MESSAGE' is not correct"
            assert obj['success'] == True, f"The value of 'TYPE' is not correct"