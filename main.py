from config import *
from output import FileOutputGenerator
from scoring_engine import *

if __name__ == '__main__':
    configLoader = FileConfigLoader()
    configs = configLoader.load("config.json")

    scoring_engine = ScoringEngine(configs, PageExtractor())
    results = scoring_engine.score_folder("folder")

    # get orientation
    # ASSUMING ALL HORIZONTAL
    for result in results:
        result.orientation = "HORIZONTAL"

    # make decision based on result
    pass_result = []
    for result in results:
        if result.status == "PASS":
            pass_result.append(result)
    # do pass

    # do fail

    # do result based on score --> now just dump all result into json
    output_generator = FileOutputGenerator("result.json")
    output_generator.process_result(pass_result)

