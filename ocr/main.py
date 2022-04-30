import json

from db import Db
from ocr import Ocr
from rabbitmq import RabbitProvider

db = Db("127.0.0.1", 3306, "root", "root", "ocr")
rabbit = RabbitProvider("localhost", 5672, "scoring")

file = "/Users/user/ocr/3.pdf"
print(f"start ocr for file: {file}")
ocr = Ocr(file, "/Users/user/ocr/output_3", db.engine)
file = ocr.run()
print("ocr done")
rabbit.publish(json.dumps(file))
print(f"published work {file}")
