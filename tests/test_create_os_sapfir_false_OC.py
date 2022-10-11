import json
from my_lib.assertions import Assertion
from my_lib.my_requests import MyRequests
from my_lib.base_case import BaseCase
import allure

# Название: Создать ОС в САПФИР
# Место положение: раздел Ввод ИТ-активов в эксплуатации
# Тест кейс: https://jira.itexpert.ru/secure/Tests.jspa#/testCase/IT4ITMVP-T2108
# Описание: https://cf.itexpert.ru/pages/viewpage.action?pageId=155490682
# Описание раздела: https://cf.itexpert.ru/pages/viewpage.action?pageId=155486811

# python -m pytest -s test_create_os_sapfir_false_OC.py -k TestCreateOS_SAPFIR_False
# python -m pytest --alluredir=allure_result_folder tests/test_create_os_sapfir_false_OC.py
# allure serve allure_result_folder

@allure.epic("Создать ОС в САПФИР. С установленным флагом 'Требуется монтаж' = False")
class TestCreateOS_SAPFIR_False(BaseCase):

    # Авторизация и получение необходимых cookie и headers
    @allure.description("Авторизация и получение необходимых cookie и headers")
    def setup(self):
        env = 'http://localmail.itexpert.ru:5057'
        auth_data = {
            "UserName": "d.vavrinyuk",
            "UserPassword": "123"
        }


        self.url = "http://192.168.0.73:44400/test/IteURLRequestSAPToCheckStock2"
        self.jar, self.header = MyRequests.user_auth(self, auth_data, env)

    # Условие: флаг "Передано в БУ" = 0 - iteRequestForCommissioningAsset.iteSendToAccountingSytem == FALSE
    # Условие: флаг "Необходим монтаж" = 1 - iteNeedForAssembling = True
    @allure.description("В запросе установлен флаг 'Требуется монтаж' iteNeedForAssembling = False")
    # 1 ИТ-активы для ввода в эксплуатацию в качестве ОС
    @allure.description("ИТ-активы для ввода в эксплуатацию в качестве ОС")
    def test_request_1(self):
        json_data = {
            "currentPage": "1",
            "pageCount": "1",
            "delta": "F",
            "item": [
                {
                    "row": "1",
                    "WERKS": "1001",            # Завод - IteRequestForCommissioningAsset.iteAsset.ItePlantCode
                    "LGORT": "IteWHCode",       # Склад - IteWHCode IteRequestForCommissioningAsset.iteAsset.IteLogisticStructure.IteWHCode
                    "MATNR": "770000070125",    # Код материала - IteRequestForCommissioningAsset.iteAsset.IteAssetDirectory.IteAssetAccountingNumber
                    "PSPPNR": "1100648.80016-YO04-00001",   # СПП-элемент - IteRequestForCommissioningAsset.iteAsset.ItePPStructure.IteItemCode
                    "CHARG": "0004566071",      # Партия(строка) - IteRequestForCommissioningAsset.iteAsset.IteConsignmentCode
                }
            ]
        }

        print(f"\n ИТ-активы для ввода в эксплуатацию в качестве ОС")
        # Проверка обязательных полей
        items = ["WERKS", "LGORT", "CHARG", "PSPPNR"]
        json_data_list = json_data["item"]
        json_data_dict = json_data_list[0]
        for key, value in json_data_dict.items():
            assert value != "", f"'Передача данных прервана, данные{key} не могут быть пустые"

        response = MyRequests.post(self.url, json=json_data, headers=self.header, cookies=self.jar)
        Assertion.assert_code_status(response, 200)

        print(response.text)

        obj = json.loads(response.text)
        for str in obj["item"]:
            for key, value in str.items():
                if key in items:
                    assert key in items and value != "", f"Передача данных в САПФИР для создания ОС не выполнена. Отсутствуют необходимые остатки на складе {str[key]}"
                # if key == "PRLAB" and value == "0":
                    # assert str[key] != "0", f"По материалу {str['MATNR']} нет необходимого остатка на складе"

    # # 2 ИТ-активы для ввода в эксплуатацию в качестве МОС
    # @allure.description("ИТ-активы для ввода в эксплуатацию в качестве МОС")
    # def test_request_2(self):
    #     json_data = {
    #         "currentPage": "1",
    #         "pageCount": "1",
    #         "delta": "F",
    #         "item": [
    #             {
    #                 "row": "1",
    #                 "WERKS": "1001",            # Завод - IteRequestForCommissioningLowAsset.iteAsset.ItePlantCode
    #                 "LGORT": "IteWHCode",       # Склад - IteWHCode IteRequestForCommissioningLowAsset.iteAsset.IteLogisticStructure.IteWHCode
    #                 "MATNR": "770000070125",    # Код материала - IteRequestForCommissioningLowAsset.iteAsset.IteAssetDirectory.IteAssetAccountingNumber
    #                 "PSPPNR": "1100648.80016-YO04-00001",   # СПП-элемент - IteRequestForCommissioningLowAsset.iteAsset.ItePPStructure.IteItemCode
    #                 "CHARG": "0004566071",      # Партия(строка) - IteRequestForCommissioningLowAsset.iteAsset.IteConsignmentCode
    #             }
    #         ]
    #     }
    #
    #     # Проверка обязательных полей
    #     items = ["WERKS", "LGORT", "CHARG", "PSPPNR"]
    #     json_data_list = json_data["item"]
    #     json_data_dict = json_data_list[0]
    #     for key, value in json_data_dict.items():
    #         assert value != "", f"'Передача данных прервана, данные{key} не могут быть пустые"
    #
    #     response = MyRequests.post(self.url, json=json_data, headers=self.header, cookies=self.jar)
    #     Assertion.assert_code_status(response, 200)
    #     # print(response.text)
    #     obj = json.loads(response.text)
    #     for str in obj["item"]:
    #         for key, value in str.items():
    #             if key in items:
    #                 assert key in items and value != "", f"Передача данных в САПФИР для создания ОС не выполнена. Отсутствуют необходимые остатки на складе {str[key]}"
    #             # if key == "PRLAB" and value == "0":
    #                 # assert str[key] != "0", f"По материалу {str['MATNR']} нет необходимого остатка на складе"

    # 3 Отправка сообщения для ввода в эксплуатацию ОС
    @allure.description("Отправка сообщения для ввода в эксплуатацию ОС")
    def test_request_3(self):

        self.url = "http://192.168.0.73:44400/test/createOS"

        json_data = {
            "currentPage": "1",  # текущая страница
            "pageCount": "1",  # количество страниц
            "delta": "F",  # F - режим полной выгрузки справочника, D - дельта(по умолчанию),
            "item":[
                {
                    "BUKRS": "1000",            # iteRequestForCommissioning.IteOwningОrganization.IteBUCode
                    "ANLKL": "10400000",        # iiteRequestForCommissioningAsset.iteAsset.IteAssetDirectory.iteAssetClass
                    "POSNR": "11000.I16GSP0119",  # iiteRequestForCommissioning.ItePPStructure.IteItemCode
                    "TXT50": "Ноутбук Dell PER440/409316Z", #Наименование справочник-ИТА iiteRequestForCommissioningAsset.iteAsset.IteAssetDirectory.IteAssetWorkingName
                    "TXA50": "",                # iiteRequestForCommissioningAsset.iteAsset.IteAssetDirectory.IteAssetWorkingName
                    "SERNR": "123Test",             # Серийный номер актива #iiteRequestForCommissioningAsset.iteAsset.IteSerialNumber
                    "INVNR": "",
                    "XNEU_AM": "",
                    "MEINS": "шт",              # единицы измерения в справочнике-ИТА iiteRequestForCommissioningAsset.iteAsset.IteAssetDirectory.IteBaseUnit,
                    "MENGE": "1.0",             # i1,
                    "GLO_RUS_OKOF16": "test123",   #Код ОКФ спрвочник-ИТА iiteRequestForCommissioningAsset.iteAsset.IteAssetDirectory.iteOKOFCode
                    "NDJAR": "2029254348",      # iiteRequestForCommissioningAsset.IteAsset.IteUsefulLife
                    "ZZPROPTYPE": "1",           # i1,
                    "AKTIV": "",                # iiteRequestForCommissioning.iteCommissioningDate,
                    "ZZTOU": "Код ТОУ",                # Код ТОУ в справчонике ИТА iiteRequestForCommissioningAsset.iteAsset.IteAssetDirectory.iteTOUCode
                    "GLO_RUS_DEPGR": "Группа амортизации",        # iiteRequestForCommissioningAsset.iteAsset.IteAssetDirectory.iteAmortizationGroup
                    "KOSTL": "2029254348",      # iiteRequestForCommissioning.IteCostCenter.IteCSCode,
                    "PERNR": "285052",        # iiteRequestForCommissioningAsset.iteAsset.IteResponsible.IteConditionalNumber.ItePersonnelNumber
                                                #(где IteConditionalNumber.IteBUCode == значение для поля "BUKRS")
                    "STORT": "KTEXT",
                    "KTEXT": "",
                    "ZZMATNR": "",
                    "INBDA": "",
                    "ZZVVOD_DOK_NAME": "",
                    "ZZVVOD_DOK_DATE": "",
                    "ZZVVOD_DOK_NUM": "",
                    "LIEFE": "",
                    "ORD43": "test",            # iteRequestForCommissioningAsset.iteAcquisitionKind.Code,
                    "ZZDOG_NUM": "",
                    "NAME_TEXT": "test_spec",  # (контакт текущей учетной записи, кто инициировал отправку сообщения в САПФИР)
                    "SMTP_ADDR": "5050@stepanov.work"  # (контакт текущей учетной записи, кто инициировал отправку сообщения в САПФИР)
                }
            ]
        }

        print(f"\n Отправка сообщения для ввода в эксплуатацию ОС")
        # проверка всех полей на заполнение
        json_data_list = json_data["item"]
        json_data_dict = json_data_list[0]
        # print(json_data_dict)
        # for key, value in json_data_dict.items():
        #     if value == "":
        #         print(key)

        assert json_data_dict["NAME_TEXT"] != "", "Параметр Code не может быть пустым."
        assert json_data_dict["SMTP_ADDR"] != "", "Параметр Name не может быть пустым."

        response = MyRequests.post(self.url, json=json_data, headers=self.header, cookies=self.jar)
        Assertion.assert_code_status(response, 200)

        print(response.text)

        obj = json.loads(response.text)
        assert obj["message"] == 'OK', f"The value of 'MESSAGE' is not correct"
        assert obj["isSuccessful"] == True, f"The value of 'success' is not correct"
        for str in obj["result"]:
            for key, value in str.items():
                if key == "TYPE":
                    assert value == "S", f"Запрос не корректен"

    # 4 Инициирована передача в САПФИР (ОС без монтажа, Предварительный акт списания)
    @allure.description("Инициирована передача в САПФИР (ОС без монтажа, Предварительный акт списания)")
    def test_request_4(self):

        self.url = "http://192.168.0.73:44400/test/CreateAct"
        json_data = {
                "currentPage": "1",
                "pageCount": "1",
                "delta": "F",
                "item": [
                    {
                        "ACT_ID_IT": "RC00000036",
                        "ACT_POS_IT": "1",
                        "BUKRS": "1000",
                        "WERKS": "0001",
                        "LGORT": "0048",
                        "MATNR": "test",
                        "PSPNR": "BD103-2014-6140101-104",
                        "CHARG": "111",
                        "MENGE": "1.0",
                        "MEINS": "",
                        "DATE_SPIS_PLAN": "27.10.2021",
                        "MSEG_BWART": "941",
                        "MSEG_KOSTL": "2029254348",
                        "MSEG_PSPNR": "",
                        "MSEG_ANLN1": "123123",
                        "MSEG_SAKTO": "3512406001",
                        "MSEG_PRICINA": ""
                    }
                ]
            }

        print(f"\n Инициирована передача в САПФИР")
        # проверка всех полей на заполнение
        # json_data_list = json_data["item"]
        # json_data_dict = json_data_list[0]
        # # print(json_data_dict)
        # for key, value in json_data_dict.items():
        #     if value == "":
        #         print(key)

        response = MyRequests.post(self.url, json=json_data, headers=self.header, cookies=self.jar)
        Assertion.assert_code_status(response, 200)

        print(response.text)

        obj = json.loads(response.text)
        assert obj["message"] == 'OK', f"The value of 'MESSAGE' is not correct"
        assert obj["isSuccessful"] == True, f"The value of 'success' is not correct"
        for str in obj["result"]:
            for key, value in str.items():
                if key == "TYPE":
                    assert value == "S", f"Запрос не корректен"


