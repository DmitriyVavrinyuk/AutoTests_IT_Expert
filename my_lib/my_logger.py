import datetime
import os
from requests import Response


class MyLogger:

    @classmethod
    def _write_log_to_file(cls, data: str, file_name: str):
        with open(file_name, 'a', encoding="utf-8") as logger_file:
            logger_file.write(data)

    @classmethod
    def add_requests(cls, url: str, data: dict, json: dict, headers: dict, cookies: dict, method: str, file_name: str, test_name: str):
        #testname = os.environ.get('PYTEST_CURRENT_TEST')
        data_to_add = f"\n------\n"
        data_to_add += f"Test: {test_name}\n"
        data_to_add += f"Time: {str(datetime.datetime.now())}\n"
        data_to_add += f"Request method: {method}\n"
        data_to_add += f"Request URL: {url}\n"
        data_to_add += f"Request data: {data}\n"
        data_to_add += f"Request json: {json}\n"
        data_to_add += f"Request cookies: {headers}\n"
        data_to_add += f"Request headers: {cookies}\n"

        data_to_add += "\n-------\n"
        cls._write_log_to_file(data_to_add, file_name)

    @classmethod
    def add_response(cls, response: Response, file_name: str):
        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)
        data_to_add = f"Response code: {response.status_code}\n"
        data_to_add += f"Response text: {response.text}\n"
        data_to_add += f"Response head: {response.headers}\n"
        data_to_add += f"Response cookies: {response.cookies}\n"
        data_to_add += "\n-------\n"
        cls._write_log_to_file(data_to_add, file_name)


