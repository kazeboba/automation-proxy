import json
import os
from jsonpath_ng.ext import parse as parse_ext


class FileWorker:
    def __init__(self):
        self.current_directory = os.path.abspath(os.path.join(os.environ["VIRTUAL_ENV"], ".."))
        self.__proxy_data = os.path.join(self.current_directory, "config.json")
        self.__response_dir = os.path.join(self.current_directory, "response")

    @staticmethod
    def __file_json_to_dict(file_path: str) -> dict:
        with open(file_path, encoding='utf-8-sig') as filestream:
            text_from_file = filestream.read()
            temp_dict = json.loads(text_from_file)
        return temp_dict

    @staticmethod
    def __write_data_to_file(file_path: str, key_write: str, value_write: any):
        with open(file_path, encoding='utf-8-sig') as filestream:
            text_from_file = filestream.read()
        read_conf = json.loads(text_from_file)
        read_conf[key_write] = value_write
        text_for_file = json.dumps(read_conf, indent=4, ensure_ascii=False, separators=(',', ':'))
        with open(file_path, 'w', encoding='utf-8-sig') as filestream:
            filestream.write(text_for_file)

    @staticmethod
    def __write_all_data_json(file_path: str, dict_to_write: dict | str):
        if not isinstance(dict_to_write, str):
            text_for_file = json.dumps(dict_to_write, indent=4, ensure_ascii=False, separators=(',', ':'))
        else:
            text_for_file = dict_to_write
        with open(file_path, 'w', encoding='utf-8-sig') as filestream:
            filestream.write(text_for_file)

    def get_proxy_params(self) -> dict:
        return self.__file_json_to_dict(self.__proxy_data)

    def set_proxy_param(self, param: str, value):
        self.__write_data_to_file(self.__proxy_data, param, value)

    @staticmethod
    def mock(params: dict, data: str) -> str | None:
        if isinstance(data, str):
            data = json.loads(data)
        modified_flag = False
        for key, new_value in params.items():
            for match in parse_ext(f'$..{key}').find(data):
                if match.value != new_value:
                    print(f"Key '{key}' = '{match.value}' modified to '{new_value}'")
                    match.full_path.update(data, new_value)
                    modified_flag = True

        if modified_flag: return json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        else: return None

    def set_proxy_temp_file(self, filename: str, data: dict | str):
        self.__write_all_data_json(os.path.join(self.current_directory, "responses", filename), json.loads(data))
