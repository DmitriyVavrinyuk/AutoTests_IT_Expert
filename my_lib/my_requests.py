import requests
from my_lib.my_logger import MyLogger
from my_lib.base_case import BaseCase
import datetime
import json.decoder
import allure

class MyRequests():
    @staticmethod
    def post(url: str, data: dict = None, json: dict = None, headers: dict = None, cookies: dict = None, test_name: str = None):
        with allure.step(f"POST request to URL '{url}'"):
            return MyRequests._send(url, data, json, headers, cookies, 'POST', test_name)

    @staticmethod
    def get(url: str, data: dict = None, json: dict = None, headers: dict = None, cookies: dict = None, test_name: str = None):
        with allure.step(f"GET request to URL '{url}'"):
            return MyRequests._send(url, data, json, headers, cookies, 'GET', test_name)

    @staticmethod
    def put(url: str, data: dict = None, json: dict = None, headers: dict = None, cookies: dict = None, test_name: str = None):
        with allure.step(f"PUT request to URL '{url}'"):
            return MyRequests._send(url, data, json, headers, cookies, 'PUT', test_name)

    @staticmethod
    def delete(url: str, data: dict = None, json: dict = None, headers: dict = None, cookies: dict = None, test_name: str = None):
        with allure.step(f"DELETE request to URL '{url}'"):
            return MyRequests._send(url, data, json, headers, cookies, 'DELETE', test_name)

    @staticmethod
    def _send(url: str, data: dict, json: dict, headers: dict, cookies: dict, method: str, test_name):
        url = f"{url}"

        if headers is None:
            headers = {}

        if cookies is None:
            cookies = {}

        file_name = f"log/log_" + str(datetime.datetime.now().strftime("%Y%m%d%H%M")) + ".log"
        MyLogger.add_requests(url, data, json, headers, cookies, method, file_name, test_name)

        if method == "GET":
            response = requests.get(url, data=data, json=json, headers=headers, cookies=cookies)
        elif method == "POST":
            response = requests.post(url, data=data, json=json, headers=headers, cookies=cookies)
        elif method == "PUT":
            response = requests.put(url, data=data, json=json, headers=headers, cookies=cookies)
        elif method == "DELETE":
            response = requests.delete(url, data=data, json=json, headers=headers, cookies=cookies)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")

        MyLogger.add_response(response, file_name)
        return response


    def user_auth(self, auth_data, env):
        url = env + '/ServiceModel/AuthService.svc/Login'

        header1 = {
            'Content-Type': "application/json",
            'User-Agent': "PostmanRuntime/7.29.0",
            'Accept': "*/*",
            'Cache-Control': "Cache-Control",
            'Host': "localmail.itexpert.ru:5057",
            'Accept-Encoding': "gzip, deflate, br",
            'Connection': "keep-alive",
            'Content-Length': "69"
        }

        response = MyRequests.post(url, json=auth_data, headers=header1)
        jar = response.cookies
        bpmcsrf = BaseCase.get_cookie(self, response, "BPMCSRF")
        header2 = {
            'Content-Type': "application/json",
            'User-Agent': "PostmanRuntime/7.29.0",
            'Accept': "*/*",
            'Cache-Control': "Cache-Control",
            'Host': "localmail.itexpert.ru:5057",
            'Accept-Encoding': "gzip, deflate, br",
            'Connection': "keep-alive",
            'Content-Length': "69",
            'BPMCSRF': bpmcsrf
        }
        return jar, header2



