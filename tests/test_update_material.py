import json
import allure
from my_lib.assertions import Assertion
import warnings
from my_lib.my_requests import MyRequests
from my_lib.base_case import BaseCase


# Название: Импорт МТР из ЕСМ
# Место положение: Рабочее место "Активы", раздел "Справочник ИТ-активов
# Тест-кейс: https://jira.itexpert.ru/secure/Tests.jspa#/testCase/IT4ITMVP-T2109
# Описание: https://cf.itexpert.ru/pages/viewpage.action?pageId=174053399

# python -m pytest -s test_update_material.py
# python -m pytest -s tests\test_update_material.py -k TestUpdateMaterial
# python -m pytest --alluredir=allure_result_folder tests/test_update_material.py
# allure serve allure_result_folder

@allure.epic("Интеграционное взаимодействие с 1С КСУ НСИ (ЕСМ). Импортируются данные по 'справочнику ИТ-активов'")
class TestUpdateMaterial(BaseCase):

# Авторизация и получение необходимых cookie и headers
# Поиск значений в справочнике осуществляется по Номенклатурный № (IteAssetAccountingNumber).  "Code"
# Если значение найдено - обновляем атрибуты, если не найдено - создаем новую запись в справочнике ИТА.
    @allure.description("Авторизация и получение необходимых cookie и headers")
    def setup(self):
        env = 'http://localmail.itexpert.ru:5055'
        auth_data = {
            "UserName": "Supervisor",
            "UserPassword": "!Supervisor123Test!"
        }

        self.url = "http://localmail.itexpert.ru:5055/rest/IteESMIntegrationService/v1/UpdateMaterial"
        self.jar, self.header = MyRequests.user_auth(self, auth_data, env)

# Запуск первой проверки: python - m pytest - s test_update_material.py - k testpdateaterial - k test_request_for_supply
    @allure.description("Поиск значений в справочнике по Номенклатурный № (IteAssetAccountingNumber)'Code'. "
                        "Если значение найдено - обновляем атрибуты в разделе 'Справочники ИТА'")
    def test_request_for_supply(self):
        json_data = {
            "Material":
                {
                #Рабочее место "Активы", раздел "Справочник ИТ-активов"
                "Code": "000001236799",     #Поле "Номенклатурный №"
                "Class": "G030101", #GUID Категории ЕСМ (Class) 12adbf4f-d553-11e1-bd21-005056ae005c
                "Name": "Комплект крепежный TLK/TLK-FPFP-50", #Поле Наименование Б/У
                "Full_Name": "Комплект крепежный (винт, шайба, гайка, упаковка 50 шт.) TLK/TLK-FPFP-50", #Поле Описание
                "UOM_Base": "071",          #Код базовой ед. измерения
                "UOM_BaseName": "071",    #Название базовой ед.измерения
                "UOM_Weight": "071",        #Код ед. измерения веса
                "UOM_Volume": "ШТ",        #Код ед. измерения объема
                "UOM_Size": "",          #Код ед. измерения размера
                "UOM_ForOrder": "",         #Код ед.измернеия для заказа на поставку
                "Weight_Netto": "1",        #Поле Вес, нетто
                "Weight_Brutto": "1",       #Вес, брутто
                "Volume": "15",             #Объем
                "Lenght": "10",             #Длмна
                "Width": "20",              #Ширина
                "Height": "15",              #Высота
                "Barcode": "",              #Эквивалентен ШтрихКод из КСУ НСИ
                "Block": False,             #эквивалентен Блокировка из КСУ НСИ – true/false, без пустых значения
                "Deletion_mark": False,     #эквивалентен ПометкаУдаления – true/false, без пустых значения
                "Manufacturer": "CAREL INDUSTRIES S.p.a",         #Изготовитель
                "Brand": "AM002540",                #Модель
                "PartNumber": "Тестовые данные для импорта"            # Парт-номер
            }
        }

        # Проверка обязательных полей
        json_data_dict = json_data["Material"]
        assert json_data_dict["Code"] != "", "Параметр Code не может быть пустым."
        assert json_data_dict["Name"] != "", "Параметр Name не может быть пустым."

        # Проверка что все данные модели введены
        items = ["Brand", "Manufacturer", "PartNumber"]
        for key, value in json_data_dict.items():
            if key in items:
                if value == "":
                    # assert json_data_dict[key] != "", f"Получены не все данные {key} по модели"
                    warnings.warn(f"Получены не все данные {key} по модели")
                print(key)


        response = MyRequests.post(self.url, json=json_data, headers=self.header, cookies=self.jar)
        Assertion.assert_code_status(response, 200)
        print(response.text)
        obj = json.loads(response.text)
        for result, value in obj.items():
            # print(result, value)
            assert obj["message"] == None, f"The value of 'message' is not correct"
            assert obj['success'] == True, f"The value of 'success' is not correct"


# # Запуск второй проверки: python - m pytest - s test_update_material.py - k testpdateaterial - k test_request_for_supply_empty_num
#     # Поле code = null создание новой записе в разделе "Справочники ИТА"
#     @allure.description("Если не найдено - создаем новую запись в справочнике ИТА.")
#     def test_request_for_supply_empty_num(self):
#         json_data = {
#             "Material":
#                 {
#                     # Рабочее место "Активы", раздел "Справочник ИТ-активов"
#                     "Code": "",  # Поле "Номенклатурный №"
#                     "Class": "G03",  # GUID Категории ЕСМ (Class) 12adbf4f-d553-11e1-bd21-005056ae005c
#                     "Name": "Комплект крепежный TLK/TLK-FPFP-50",  # Поле Наименование Б/У
#                     "Full_Name": "Комплект крепежный (винт, шайба, гайка, упаковка 50 шт.) TLK/TLK-FPFP-50",
#                     # Поле Описание
#                     "UOM_Base": "001",  # Код базовой ед. измерения
#                     "UOM_BaseName": "ШТ",  # Название базовой ед.измерения
#                     "UOM_Weight": "002",  # Код ед. измерения веса
#                     "UOM_Volume": "003",  # Код ед. измерения объема
#                     "UOM_Size": "003",  # Код ед. измерения размера
#                     "UOM_ForOrder": "004",  # Код ед.измернеия для заказа на поставку
#                     "Weight_Netto": "1",  # Поле Вес, нетто
#                     "Weight_Brutto": "1",  # Вес, брутто
#                     "Volume": "15",  # Объем
#                     "Lenght": "10",  # Длмна
#                     "Width": "20",  # Ширина
#                     "Height": "5",  # Высота
#                     "Barcode": "",  # Эквивалентен ШтрихКод из КСУ НСИ
#                     "Block": False,  # эквивалентен Блокировка из КСУ НСИ – true/false, без пустых значения
#                     "Deletion_mark": False,  # эквивалентен ПометкаУдаления – true/false, без пустых значения
#                     "Manufacturer": "1С",  # Изготовитель
#                     "Brand": "AM002540",  # Модель
#                     "PartNumber": "Тестовые данные для импорта"  # Парт-номер
#                 }
#         }
#
#         # Проверка обязательных полей
#         json_data_dict = json_data["Material"]
#         # assert json_data_dict["Code"] != "", "Параметр Code не может быть пустым."
#         assert json_data_dict["Name"] != "", "Параметр Name не может быть пустым."
#
#         # Проверка что все данные модели введены
#         items = ["Brand", "Manufacturer", "PartNumber"]
#         for key, value in json_data_dict.items():
#             if key in items:
#                 if value == "":
#                     # assert json_data_dict[key] != "", f"Получены не все данные {key} по модели"
#                     warnings.warn(f"Получены не все данные {key} по модели")
#                 print(key)
#
#         response = MyRequests.post(self.url, json=json_data, headers=self.header, cookies=self.jar)
#         Assertion.assert_code_status(response, 200)
#         print(response.text)
#         obj = json.loads(response.text)
#         print(type(obj))
#         # for result in obj:
#         #     print(result)
#         #     assert result['message'] == "", f"The value of 'MESSAGE' is not correct"
#         #     assert result['isSuccessful'] == "true", f"The value of 'TYPE' is not correct"

