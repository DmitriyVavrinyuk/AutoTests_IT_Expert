import json
from my_lib.assertions import Assertion
from my_lib.my_requests import MyRequests
from my_lib.base_case import BaseCase
import allure

# Название: Счет-фактура (Автоматическая регистрация запроса на поставку по сообщению из САПФИР )
# Место положение: Раздел "Поставка ИТ-активов"
# Описание: https://cf.itexpert.ru/pages/viewpage.action?pageId=151191597

# python -m pytest -s test_update_invoice.py
# python -m pytest -s tests\test_update_invoice.py
# python -m pytest --alluredir=allure_result_folder tests/test_update_invoice.py
# allure serve allure_result_folder

@allure.epic("Счет-фактура (Автоматическая регистрация запроса на поставку по сообщению из САПФИР. Раздел 'Поставка ИТ-активов'")
class TestUpdateInvoice(BaseCase):

    @allure.description("Авторизация и получение необходимых cookie и headers")
    def setup(self):
        env = 'http://localmail.itexpert.ru:5057'
        auth_data = {
            "UserName": "Supervisor",
            "UserPassword": "!Supervisor123Test!"
        }
        self.url = "http://localmail.itexpert.ru:5057/rest/SapErpIntegrationService/v1/UpdateInvoice"
        self.jar, self.header = MyRequests.user_auth(self, auth_data, env)

    # Система ищет экземляр IteRequestForPurchaseAsset
    #
    @allure.description("Счет-фактура (Автоматическая регистрация запроса на поставку по сообщению из САПФИР")
    @allure.description("Запрос на поставку создается только один раз на основании параметров первой строки сообщения от SAP PO"
                        "Система ищет экземляр IteRequestForPurchaseAsset по условию:")
    def test_request_for_supply(self):
        json_data = {
                    "currentPage": "1",
                    "pageCount": "1",
                    "delta": "D",
                    "item": [
                        {
                            "row": "1",               # Номер строки внутри передаваемого НД
                            "BLART": "t1",            # Вид документа
                            "BELNR": "SAP 1",         # IteInvoiceSAP (Номер документа счета-фактуры)
                            "GJAHR": "2021",          # IteFinYear (Финансовый год)
                            "XBLNR": "Supplier 1",    # IteInvoiceSupplier (Номер счет-фактуры)
                            "BUKRS": "1111",          # ItePayer (Организация-собственник) == (SysAdminUnit).IteBUCode (Код балансовой единицы)
                            # "LIFNR": "0000029312",    # IteSupplier (Поставщик) == сопоставление по Объект Контрагенты.Code
                            "LIFNR": "Test code",   # IteConsigner (Грузоотправитель) == сопоставление по Объект Контрагенты.Code
                            "BLDAT": "01.02.2020",    # IteInvoiceDate (Дата счет-фактур)
                            "BUDAT": "01.01.2020",    # IteInvoicePostingDate (Дата проводки СФ)
                            "BUZEI": "100001",        # Деталь "ИТ-активы" IteInvoicePosSAP (Позиция в документе SAP)
                            "EBELN": "Order test",    # ItePurchaseOrder (Заказ на закупку / План МТО)
                            # (первая запись IteRequestForPurchaseAsset.IteRequestForPurchase из выборки IteRequestForPurchaseAsset.IteOrder == EBELN),
                            # если выборка пустая то (первая запись IteRequestForPurchaseAssetComponent.IteRequestForPurchase из
                            # выборки IteRequestForPurchaseAssetComponent.IteOrder == EBELN)

                            "EBELP": "10000",         # ItePurchaseOrderPos (Позиция запроса на закупку) в детале "ИТ-актив" ItePurchaseOrderPosSAP (Позиция документа закупки)
                            "MATNR": "test1705-2",  # Материал
                            "WERKS": "1001",        # Завод
                            "MENGE": "10.1",        # Количество
                            "BSTME": "ШТ",          # Единица измерения материала в заказе
                            "DPROG": "01.03.2020",  # IteExpectedDate (Прогнозная дата поставки)
                            "MEINS": "qwe",         # Базовая единица измерения материала
                            "MEINH": "qwe",         # Альтернативная складской единица измерения
                            "UMREZ": "10000",       # Числитель для пересчета альтернативной ЕИ в базисную ЕИ
                            "UMREN": "10002",       # Знаменатель для пересчета альтернативной ЕИ  в базисную ЕИ
                            "RBSTAT": "q",          # Статус
                            "STBLG": "test test2",  # Документ сторно
                            "STJAH": "1000",        # Год документа сторно
                            "ZZ_ZEMLI": "CodeSAP 11",   # IteConsignees (Грузополучатель) == сопоставление по Грузополучатели (IteConsignees).IteCodeConsignees
                            "NETPR": "12.5",            # Цена позиции за единицу измерения материала в заказе
                            "WRBTR": "50001.00",        # Стоимость позиции
                            "deleted": "false"
                        }
                    ]
                }
    #
        exceptions = ""
        json_data_list = json_data["item"]
        json_data_dict = json_data_list[0]

        # Проверка что все поля заполнены.
        for key, value in json_data_dict.items():
            if value == "":
                exceptions += f"{key}, "
                print(f"Отсутствуют значения в атрибутах: {exceptions} ")
            assert json_data_dict[key] != "", f"Отсутствуют значения в атрибутах: '{key}' "

        # Проверка заполнение ключей
        items = ["BUKRS", "LIFNR", "ZZ_ZEMLI", "MATNR", "RBSTAT", "WERKS"]
        for key, value in json_data_dict.items():
            if key in items and value == "":
                    print(key)
                    assert json_data_dict[key] != "", f"В системе не найдено соответствий для атрибутов: {key} "

        # assert json_data_dict[""] != None, "bnm"

        response = MyRequests.post(self.url, json=json_data, headers=self.header, cookies=self.jar)
        Assertion.assert_code_status(response, 200)
        print(response.text)
        obj = json.loads(response.text)
        for result in obj['result']:
            assert result['MESSAGE'] == "", f"The value of 'MESSAGE' is not correct"
            assert result['TYPE'] == "S", f"The value of 'TYPE' is not correct"
            print("Запрос на поставку сформирован ")




    # def test_request_for_supply_asset(self):
    #     json_data = {
    #         "currentPage": "1",
    #         "pageCount": "1",
    #         "delta": "D",
    #         "item": [
    #             {
    #               "row": "1",
    #               "BLART": "t1",
    #               "BELNR": "SAP 1",         # IteInvoiceSAP (Номер СФ)
    #               "GJAHR": "2021",          # IteFinYear (Финансовый год)
    #               "XBLNR": "Supplier 1",    # IteInvoiceSupplier (Номер счет-фактуры)
    #               "BUKRS": "1111",          # ItePayer (Организация-собственник) == (SysAdminUnit).IteBUCode (Код балансовой единицы)
    #               "LIFNR": "Test code",     # IteSupplier (Поставщик) == сопоставление по Объект Контрагенты.Code
    #               # "LIFNR": "Test code",   # IteConsigner (Грузоотправитель) == сопоставление по Объект Контрагенты.Code
    #               "BLDAT": "01.02.2020",    # IteInvoiceDate (Дата счет-фактур)
    #               "BUDAT": "01.01.2020",    # IteInvoicePostingDate (Дата проводки СФ)
    #               "BUZEI": "100001",        # Деталь "ИТ-активы" IteInvoicePosSAP (Позиция в документе SAP)
    #               "EBELN": "Order test",    # ItePurchaseOrder (Заказ на закупку / План МТО)
    #                 # (первая запись IteRequestForPurchaseAsset.IteRequestForPurchase из выборки IteRequestForPurchaseAsset.IteOrder == EBELN),
    #                 # если выборка пустая то (первая запись IteRequestForPurchaseAssetComponent.IteRequestForPurchase из
    #                 # выборки IteRequestForPurchaseAssetComponent.IteOrder == EBELN)
    #               "EBELP": "10000",         # ItePurchaseOrderPos (Позиция запроса на закупку) в детале "ИТ-актив" ItePurchaseOrderPosSAP (Позиция документа закупки)
    #               "MATNR": "test1705-2",
    #               "WERKS": "1001",
    #               "MENGE": "10.1",
    #               "BSTME": "ШТ",
    #               "DPROG": "01.03.2020",   # IteExpectedDate (Прогнозная дата поставки)
    #               "MEINS": "qwe",
    #               "MEINH": "qwe",
    #               "UMREZ": "10000",
    #               "UMREN": "10002",
    #               "RBSTAT": "q",
    #               "STBLG": "test test2",
    #               "STJAH": "1000",
    #               "ZZ_ZEMLI": "CodeSAP 11",     # IteConsignees (Грузополучатель) == сопоставление по Грузополучатели (IteConsignees).IteCodeConsignees
    #               "NETPR": "12.5",
    #               "deleted": ""
    #             }
    #         ]
    #     }
    # # """
    #
    #     response = MyRequests.post(self.url, json=json_data, headers=self.header, cookies=self.jar)
    #     Assertion.assert_code_status(response, 200)
    #     print(response.text)
    #     obj = json.loads(response.text)
    #     print(obj)