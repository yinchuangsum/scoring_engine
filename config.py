import json


class Keyword:
    def __init__(self, name, score):
        self.name = name
        self.score = score


class Config:
    def __init__(self, sheet_name, threshold, keywords):
        self.sheet_name = sheet_name
        self.threshold = threshold
        self.keywords = keywords


class FileConfigLoader:
    def __init__(self):
        self.file = None

    def load(self, file):
        return self.__parse_data(file)

    def __parse_data(self, file):
        with open(file) as f:
            data_list = json.loads(f.read())
        configs = {}

        if type(data_list) is not list:
            raise Exception("Config file should be a json list!")

        for data in data_list:
            config = self.__parse_single_config(data)
            configs[config.sheet_name] = config

        return configs

    def __parse_single_config(self, data):
        sheet_name = data["sheet_name"]
        self.__validate_not_null(sheet_name, "sheet_name")

        threshold = data["threshold"]
        self.__validate_not_null(threshold, "threshold")

        if type(threshold) is not int:
            raise Exception("field [threshold] should be an integer")

        keywords = data["keywords"]
        self.__validate_not_null(keywords, "keywords")

        if type(keywords) is not list:
            raise Exception("field [keywords] should be a list")

        config_keywords = []
        for keyword in keywords:
            config_keywords.append(self.__parse_single_keyword(keyword))

        return Config(sheet_name, threshold, config_keywords)

    def __parse_single_keyword(self, data):
        name = data["keyword"]
        self.__validate_not_null(name, "keyword")

        score = data["score"]
        self.__validate_not_null(score, "score")

        if type(score) is not int:
            raise Exception("field [score] should be an integer")

        return Keyword(name, score)

    def __validate_not_null(self, field, field_name):
        if field is None:
            raise Exception(f"field [{field_name}] should not be null!")
