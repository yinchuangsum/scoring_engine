from sqlalchemy.orm import sessionmaker

from config import *
from db import Db, Page
from scoring_engine import *

if __name__ == '__main__':
    db = Db("127.0.0.1", 3306, "root", "root", "ocr")
    session_maker = sessionmaker()
    session_maker.configure(bind=db.engine)

    file_id = 5
    folder = "output"

    configLoader = FileConfigLoader()
    configs = configLoader.load("config.json")

    scoring_engine = ScoringEngine(configs, PageExtractor())
    results = scoring_engine.score_folder(folder)

    session = session_maker()
    for result in results:
        page = session.query(Page).filter_by(file_id=file_id, page=result.page).first()
        page.score = result.score
        page.sheet = result.sheet
        page.done_by = "SYSTEM"
        page.status = result.status
        session.flush()
    session.commit()
    session.close()



