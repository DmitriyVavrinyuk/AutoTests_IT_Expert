import json
from my_lib.assertions import Assertion
from my_lib.my_requests import MyRequests
from my_lib.base_case import BaseCase
import allure

# Название: Импорт категорий МТР из ЕСМ
# Место положение: Справочник 'Категории ЕСМ'
# Тест кейс: https://jira.itexpert.ru/secure/Tests.jspa#/testCase/IT4ITMVP-T2108
# Описание: https://cf.itexpert.ru/pages/viewpage.action?pageId=174053397&sortBy=name&sortOrder=ascending

# python -m pytest -s test_update_class.py -k TestUpdateClass
# python -m pytest -s tests\test_update_class.py -k TestUpdateClass.test
# python -m pytest --alluredir=allure_result_folder tests/test_update_class.py
# allure serve allure_result_folder

@allure.epic("Импорт категорий МТР из ЕСМ. Запрос создает запись в C")
class TestUpdateClass(BaseCase):

    # Авторизация и получение необходимых cookie и headers
    # Запрос создает запись в справочнике 'Категории ЕСМ'
    @allure.description("Авторизация и получение необходимых cookie и headers"
                        "Запрос создает запись в справочнике 'Категории ЕСМ'")
    def setup(self):
        env = 'http://localmail.itexpert.ru:5057'
        auth_data = {
            "UserName": "d.vavrinyuk",
            "UserPassword": "123"
        }
        self.url = "http://localmail.itexpert.ru:5057/rest/IteESMIntegrationService/v1/UpdateClass"
        self.jar, self.header = MyRequests.user_auth(self, auth_data, env)

    # Поиск значений в справочнике осуществляется по Поле Код "Code"
    # Если значение найдено - обновляем атрибуты, если не найдено - создаем новую запись в справочнике "Категории ЕСМ"
    # Если "Deletion_mark": "True" то запись с соответсвующем Код КСУ НСИ буде удалена
    @allure.description("Поиск записи в справочнике осуществяется по полю 'Code',"
                        "Если значение не найдено - содается запись."
                        "Если найдена - обновляется атрибут")
    def test_request_for_supply(self):

        json_data = {
            "Class": #Категории материалов
                {
                    "Name": "Арматура нагнетательная2",
                    "Full_Name": "Арматура нагнетательная",
                    "Deletion_mark": "true",
                    "Owner": "001",
                    "Parent": "febe2a32-d552-11e1-bd21-005056ae005c",
                    "Code": "G0301011"
                }
            }

        # Проверка обязательных полей
        json_data_dict = json_data["Class"]
        assert json_data_dict["Code"] != "", "Параметр Code не может быть пустым."
        assert json_data_dict["Name"] != "", "Параметр Name не может быть пустым."

        response = MyRequests.post(self.url, json=json_data, headers=self.header, cookies=self.jar)
        Assertion.assert_code_status(response, 200)
        print(response.text)
        obj = json.loads(response.text)
        # print(obj)
        for result, value in obj.items():
            # print(result, value)
            assert obj["message"] == None, f"The value of 'MESSAGE' is not correct"
            assert obj['success'] == True, f"The value of 'success' is not correct"


