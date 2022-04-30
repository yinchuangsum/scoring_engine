from sqlalchemy.orm import sessionmaker

from config import *
from db import Db, Page
from rabbitmq import RabbitConsumer
from scoring_engine import *

if __name__ == '__main__':
    db = Db("127.0.0.1", 3306, "root", "root", "ocr")
    rabbit = RabbitConsumer("127.0.0.1", 5672, "scoring")
    session_maker = sessionmaker()
    session_maker.configure(bind=db.engine)

    configLoader = FileConfigLoader()
    configs = configLoader.load("config.json")
    scoring_engine = ScoringEngine(configs, PageExtractor())

    def callback(ch, method, properties, body):
        data = json.loads(body)
        file_id = data["id"]
        folder = data["folder_location"]
        print(f"processing file {data['file_path']}")
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
        ch.basic_ack(delivery_tag=method.delivery_tag) # tell queue success
        print("process done")

    rabbit.set_callback(callback)



