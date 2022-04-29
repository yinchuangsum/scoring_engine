import json


class FileOutputGenerator:
    def __init__(self, file_name):
        self.file_name = file_name

    def process_result(self, results):
        json_results = []
        for result in results:
            json_results.append(self.result_to_dict(result))
        output = json.dumps(json_results)
        with open(self.file_name, 'w') as f:
            f.write(output)

    def result_to_dict(self, result):
        json_result = {"page_num": result.page, "orientation": result.orientation, "score": result.score,
                       "sheet": result.sheet, "done_by": result.done_by}
        return json_result
