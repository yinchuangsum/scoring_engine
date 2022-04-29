from db import Db
from ocr import Ocr

db = Db("127.0.0.1", 3306, "root", "root", "ocr")

ocr = Ocr("1.pdf", "output", db.engine)
ocr.run()
