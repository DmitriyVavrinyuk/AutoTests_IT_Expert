import json
from my_lib.assertions import Assertion
from my_lib.my_requests import MyRequests
from my_lib.base_case import BaseCase
import allure

# Название: Замена позиций в запросе на закупку
# Место положение: Раздел "Подготовка к закупке ИТ-активов"
# Описание: https://cf.itexpert.ru/pages/viewpage.action?pageId=165187694

# python -m pytest -s test_update_request.py -k TestUpdateRequestUB
# python -m pytest -s tests\test_update_request.py -k TestUpdateRequestUB
# python -m pytest --alluredir=allure_result_folder tests/test_update_request.py

@allure.epic("Обновление запроса на закупку из SAP ERP САПФИР")
class TestUpdateRequestUB(BaseCase):
# Система ищет экземляр IteRequestForPurchaseAsset
# по условию IteRequestForPurchaseAsset.IteNumber == BNFPO_IT  &&
# IteRequestForPurchaseAsset.iteIteRequestForPurchase.IteNumber == BANFN_IT
    @allure.description("Авторизация и получение необходимых cookie и headers")
    def setup(self):
        env = 'http://localmail.itexpert.ru:5057'
        auth_data = {
            "UserName": "Supervisor",
            "UserPassword": "!Supervisor123Test!"
        }

        self.url = "http://localmail.itexpert.ru:5057/rest/SapErpIntegrationService/v1/UpdateRequestUB"
        self.jar, self.header = MyRequests.user_auth(self, auth_data, env)

# Система ищет экземляр IteRequestForPurchaseAsset
# по условию IteRequestForPurchaseAsset.IteNumber == BNFPO_IT  &&
# IteRequestForPurchaseAsset.iteIteRequestForPurchase.IteNumber == BANFN_IT

#     @allure.description("Система ищет экземляр IteRequestForPurchaseAsset"
#                         "по условию IteRequestForPurchaseAsset.IteNumber == BNFPO_IT  &&"
#                         "IteRequestForPurchaseAsset.iteIteRequestForPurchase.IteNumber == BANFN_IT")
    """
        def test_correct_auth(self):
        json_data = {
            "currentPage": "1",
            "pageCount": "1",
            "delta": "F",
            "item": [
                {
                    "row": "1",
                    "BANFN_IT": "RP00000030",   # Номер потребности в СУИТА
                    "BNFPO_IT": "2",    # Позиция потребности в СУИТА
                    "BANFN": "0010017683",  # Номер корректируемой заявки подразделения (вида UB)
                    "BNFPO": "00020",       # Номер позиции корректируемой заявки подразделения (вида UB)
                    # "BANFN": "0010017683",  # Номер корректирующей заявки подразделения (вида UB)
                    "ZZ_BNFPO": "00010",    # Номер позиции корректирующей заявки подразделения (вида UB)
                    "PS_PSP_PNR": "010001.000.RE-33-0000-01",   # Код СПП-элемента
                    "MATNR": "770000023154",    # № материала в SAP
                    "MENGE": "5000.0",        # Количество материала
                    "MEINS": "ШТ",          # Единица измерения
                    "ZZ_KLASS": "",         # Класс оценки
                    "FISTL": "100117000",   # ПФМ
                    "GEBER": "NOPROJECT",   # Фонд
                    "FIPOS": "6070101",     # Финансовая позиция
                    "PREIS": "46000.00",    # Плановая цена
                    "ZEBKN": "46000.00",    # Вид контировки
                    "AUFNR": "46000.00",    # Заказ
                    "KOSTL": "46000.00",    # МВЗ
                    "ANLN1": "Q",           # Основное средство
                    "KNTTP": "Q",           # Номер потребности в СУИТА
                    "deleted": ""           # Номер потребности в СУИТА
                }
            ]
        }
    """


# Проверка IsMaterialKit == Да (Материал-комплект = Thue)
# IteRequestForPurchaseAssetComponent (Деталь "Комплектующие") -> IteAssetRequired (Закупаемая позиция) ->
# IteAssetAccountingNumber == Номенклатурный №
# Все данные вписываются в деталь IteRequestForPurchaseAssetComponent.

    # @allure.description ("IsMaterialKit == Да (Материал-комплект = Thue)"
    #                      "IteRequestForPurchaseAssetComponent (Деталь 'Комплектующие') -> IteAssetRequired (Закупаемая позиция) ->"
    #                      "IteAssetAccountingNumber == Номенклатурный №"
    #                      "Все данные вписываются в деталь IteRequestForPurchaseAssetComponent.")
    #
    # def test_correct_auth_MaterialKit_True(self):
#         json_data = {
#             "currentPage": "1",
#             "pageCount": "1",
#             "delta": "F",
#             "item": [
#                 {
#                     "row": "1",
#                     "BANFN_IT": "RP00000030",  # Номер потребности в СУИТА
#                     "BNFPO_IT": "2",  # Позиция потребности в СУИТА
#                     "BANFN": "0010017683",  # Номер корректируемой заявки подразделения (вида UB)
#                     "BNFPO": "00020",  # Номер позиции корректируемой заявки подразделения (вида UB)
#                     # "BANFN": "0010017683",  # Номер корректирующей заявки подразделения (вида UB)
#                     "ZZ_BNFPO": "00010",  # Номер позиции корректирующей заявки подразделения (вида UB)
#                     "PS_PSP_PNR": "010001.000.RE-33-0000-01",  # Код СПП-элемента
#                     "MATNR": "770000023154",  # № материала в SAP
#                     "MENGE": "5000.0",  # Количество материала
#                     "MEINS": "ШТ",  # Единица измерения
#                     "ZZ_KLASS": "1",  # Класс оценки
#                     "FISTL": "100117000",  # ПФМ
#                     "GEBER": "NOPROJECT",  # Фонд
#                     "FIPOS": "6070101",  # Финансовая позиция
#                     "PREIS": "99999.00",  # Плановая цена
#                     "ZEBKN": "46000.00",  # Вид контировки
#                     "AUFNR": "46000.00",  # Заказ
#                     "KOSTL": "46000.00",  # МВЗ
#                     "ANLN1": "Q",  # Основное средство
#                     "KNTTP": "Q",  # Номер потребности в СУИТА
#                     "deleted": "1"  # Номер потребности в СУИТА
#                 }
#             ]
#         }
#
#         # {
#         #     "row": "1",
#         #     "BANFN_IT": "RP00000030",   # Номер потребности в СУИТА
#         #     "BNFPO_IT": "2",            # Позиция потребности в СУИТА
#         #     "BANFN": "0010017683",      # iteZZMT  (Номер заявки на закупку (плана МТО)
#         #     "BNFPO": "00020",           # iteZZMTPos  (Номер позиции заявки на закупку (плана МТО)
#         #     "MATNR": "770000023154",    # IteAssetAccountingNumber = Номенклатурный №
#         #     "MENGE": "12",              # IteQtyApproved (Количество согласованное)
#         #     "FRGZU": "ШТ",              # IteZZMTStatus (Статус заявки на закупку (плана МТО)
#         #     "PREIS": "46000.00",        # IteContractPrice (Цена в контракте)
#         #
#         # }
#
#         # Проверка что все поля заполнены.
#         exceptions = ""
#         json_data_list = json_data["item"]
#         json_data_dict = json_data_list[0]
#         # print(json_data_dict)
#         items = ["row", "BANFN_IT", "BNFPO_IT", "BANFN", "BNFPO", "MATNR", "MENGE", "MEINS"]
#
#         for key, value in json_data_dict.items():
#             if value == "":
#                 exceptions += f"{key}, "
#                 # exceptions.append(key)
#                 assert json_data_dict[key] != "", f"Отсутствуют значения в атрибутах: {key} "
#         print(f"Отсутствуют значения в атрибутах: {exceptions} ")
#
#         response = MyRequests.post(self.url, json=json_data, headers=self.header, cookies=self.jar)
#         Assertion.assert_code_status(response, 200)
#         obj = json.loads(response.text)
#         for result in obj['result']:
#             assert result['MESSAGE'] == "Запись актуальна", f"The value of 'MESSAGE' is not correct"
#             assert result['TYPE'] == "I", f"The value of 'TYPE' is not correct"

# Проверка IsMaterialKit == Нет
#IsMaterialKit == Нет (Материал-комплект = False)
#IteRequestForPurchaseAssetComponent (Деталь "Комплектующие") -> iteAssetDirectory (Справочник ИТ-активов) ->
#IteAssetAccountingNumber == Номенклатурный №
#Далее все данные вписыватся в IteRequestForPurchaseAsset
#IteAssetAccountingNumber

    @allure.description("IsMaterialKit == Да (Материал-комплект = False)"
                        "IteRequestForPurchaseAssetComponent (Деталь 'Комплектующие') -> IteAssetRequired (Закупаемая позиция) ->"
                        "IteAssetAccountingNumber == Номенклатурный №"
                        "Далее все данные вписыватся в IteRequestForPurchaseAsset IteAssetAccountingNumber")
    def test_correct_auth_MaterialKit_False(self):
        json_data = {
            "currentPage": "1",
            "pageCount": "1",
            "delta": "F",
            "item": [
                {
                    "row": "",
                    "BANFN_IT": "RP00000030",  # Номер потребности в СУИТА
                    "BNFPO_IT": "3",  # Позиция потребности в СУИТА
                    "BANFN": "0010017683",  # Номер корректируемой заявки подразделения (вида UB)
                    "BNFPO": "00020",  # Номер позиции корректируемой заявки подразделения (вида UB)
                    # "BANFN": "0010017683",  # Номер корректирующей заявки подразделения (вида UB)
                    "ZZ_BNFPO": "00010",  # Номер позиции корректирующей заявки подразделения (вида UB)
                    "PS_PSP_PNR": "010001.000.RE-33-0000-01",  # Код СПП-элемента
                    "MATNR": "770000023154",  # № материала в SAP
                    "MENGE": "5000.0",  # Количество материала
                    "MEINS": "ШТ",  # Единица измерения
                    "ZZ_KLASS": "1",  # Класс оценки
                    "FISTL": "100117000",  # ПФМ
                    "GEBER": "NOPROJECT",  # Фонд
                    "FIPOS": "6070101",  # Финансовая позиция
                    "PREIS": "10.00",  # Плановая цена
                    "ZEBKN": "46000.00",  # Вид контировки
                    "AUFNR": "46000.00",  # Заказ
                    "KOSTL": "70000.00",  # МВЗ
                    "ANLN1": "Q",  # Основное средство
                    "KNTTP": "Q",  # Номер потребности в СУИТА
                    "deleted": "1"  # Номер потребности в СУИТА
                }
            ]
        }
                # {
                #     "row": "1",
                #     "BANFN_IT": "RP00000030",   # Номер потребности в СУИТА
                #     "BNFPO_IT": "3",            # Позиция потребности в СУИТА
                #     "BANFN": "0010017683",      # iteZZMT  (Номер заявки на закупку (плана МТО)
                #     "BNFPO": "00020",           # iteZZMTPos  (Номер позиции заявки на закупку (плана МТО)
                #     "MATNR": "770000605745",    # IteAssetAccountingNumber = Номенклатурный №
                #     "MENGE": "5",               # IteQtyApproved (Количество согласованное)
                #     "FRGZU": "ШТ",              # IteZZMTStatus (Статус заявки на закупку (плана МТО)
                #     "PREIS": "84000.00",        # IteContractPrice (Цена в контракте)
                #     "ANLN1": ""                 # IteFixedAsset (Основное средство)
                # }

        # Проверка что все поля заполнены.
        exceptions = ""
        json_data_list = json_data["item"]
        json_data_dict = json_data_list[0]
        # print(json_data_dict)
        items = ["row", "BANFN_IT", "BNFPO_IT", "BANFN", "BNFPO", "MATNR", "MENGE", "MEINS"]
        # Проверка если пустой ключ
        for key, value in json_data_dict.items():
            if key in items:
                if value == "":
                    print(value)
                    assert json_data_dict[key] != "", f"Key {key} isn't empty"
                print(key)


        response = MyRequests.post(self.url, json=json_data, headers=self.header, cookies=self.jar)
        Assertion.assert_code_status(response, 200)
        print(response.text)
        obj = json.loads(response.text)
        for result in obj['result']:
            assert result['MESSAGE'] == "Запись актуальна", f"The value of 'MESSAGE' is not correct"
            assert result['TYPE'] == "I", f"The value of 'TYPE' is not correct"








