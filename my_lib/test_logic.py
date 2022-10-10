import requests
import json.decoder

env = 'http://localmail.itexpert.ru:5057'
auth_data = {
    "UserName": "Supervisor",
    "UserPassword": "!Supervisor123Test!"
}

url2 = "http://localmail.itexpert.ru:5057/rest/SapErpIntegrationService/v1/UpdateRequestUB"

url = env + '/ServiceModel/AuthService.svc/Login'

header1 = {
        'Content-Type': "application/json",
        'User-Agent': "PostmanRuntime/7.29.0",
        'Accept': "*/*",
        'Cache-Control': "Cache-Control",
        'Host': "localhost:83",
        'Accept-Encoding': "gzip, deflate, br",
        'Connection': "keep-alive",
        'Content-Length': "69"
    }
response = requests.post(url,  json=auth_data, headers=header1)
jar = response.cookies
bpmcsrf = response.cookies["BPMCSRF"]
header = {
        'Content-Type': "application/json",
        'User-Agent': "PostmanRuntime/7.29.0",
        'Accept': "*/*",
        'Cache-Control': "Cache-Control",
        'Host': "localhost:83",
        'Accept-Encoding': "gzip, deflate, br",
        'Connection': "keep-alive",
        'Content-Length': "69",
        'BPMCSRF': bpmcsrf
    }

json_data = {
    "currentPage": "1",
    "pageCount": "1",
    "delta": "F",
    "item": [
        {
            "ROW": "1",
            "BANFN_IT": "RP00000028",
            "BNFPO_IT": "00010",
            "BANFN": "test",
            "BANFPO": "Test",
            "ZZ_BNFPO": "date",
            "PS_PSP_PNR": "string",
            "MATNR": "string",
            "MENGE": "double",
            "MEINS": "string",
            "ZZ_KLASS": "string",
            "FISTL": "string",
            "GEBER": "string",
            "FIPOS": "string",
            "PREIS": "string",
            "ZEBKN": "int",
            "AUFNR": "string",
            "KOSTL": "string",
            "ANLN1": "string",
            "FRGZU": "string"
        }
    ]
}

response = requests.post(url2,   json=json_data, headers=header, cookies=jar)
obj = json.loads(response.text)
print(obj)