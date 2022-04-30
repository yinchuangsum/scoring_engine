import os
import re


class ScoreEngineResult:
    def __init__(self, page, score, sheet, status):
        self.page = page
        self.score = score
        self.sheet = sheet
        self.status = status
        self.done_by = "SYSTEM"


class PageExtractor:
    def extract_page_number(self, file_name):
        return re.findall(r'\d+', file_name)[-1]


class ScoringEngine:
    def __init__(self, configs, page_extractor):
        self.configs = configs
        self.page_extractor = page_extractor

    def score_folder(self, folder):
        results = []
        for file in os.listdir(folder):
            if not file.endswith("txt"):
                continue
            print(f"scoring file {file}")
            results.append(self.score_file(os.path.join(os.path.abspath(folder), file)))
        return results

    def score_file(self, file):
        with open(file) as f:
            txt = f.read().lower()
            page = self.page_extractor.extract_page_number(file)
            return self.score_txt(txt, page)

    def score_txt(self, txt, page):
        score = 0
        sheet = ""
        status = "FAIL"
        for config in self.configs.values():
            new_score = self.score_txt_single_config(txt, config)
            new_status = self.pass_fail_single_config(new_score, config)
            if new_status == "PASS" and status == "FAIL":
                score = new_score
                sheet = config.sheet_name
                status = new_status
            elif new_score > score:
                score = new_score
                sheet = config.sheet_name

        return ScoreEngineResult(page, score, sheet, status)

    def score_txt_single_config(self, txt, config):
        score = 0
        for keyword in config.keywords:
            if keyword.name.lower() in txt:
                score += keyword.score
        return score

    def pass_fail_single_config(self, new_score, config):
        if new_score >= config.threshold:
            return "PASS"
        return "FAIL"
