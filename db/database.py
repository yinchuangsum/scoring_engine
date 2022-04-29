from sqlalchemy import create_engine


class Db:
    def __init__(self, ip, port, user, password, db):
        self.engine = create_engine(f"mysql://{user}:{password}@{ip}:{port}/{db}")
