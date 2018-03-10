from api import db


class Counter(db.Model):
    __tablename__ = 'counters'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(45), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __init__(self, title):
        self.title = title
        self.count = 0

    def add_and_commit(self):
        """
            Add and commit the counter to database.
        """
        db.session.add(self)
        db.session.commit()

    def delete_and_commit(self):
        """
            Delete the counter from the database.
        """
        db.session.query(Counter).filter(Counter.id == self.id).delete()
        db.session.commit()

    @staticmethod
    def commit():
        """
            Commit any changes to the database.
        """
        db.session.commit()

    def to_dict(self):
        """
            Return dictionary representation of model.
        :return:
        """
        return {'id': self.id, 'title': self.title, 'count': self.count}

    @classmethod
    def get_all(cls):
        """
            Get all Counter instances from the database.
        """
        return db.session.query(Counter).all()
