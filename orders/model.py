from . import db

'''
SQLAlchemy models are defined in this file.
A to Many-to-Many Relationship is used to define the relashionship between
Workers and WorkOrders.
A Worker can work on many WorkOrders
A WorkOrder can have multiple Workers.
'''


work_order_workers = db.Table(
    'work_order_workers',
    db.Column('work_order_id', db.Integer, db.ForeignKey(
        'work_order.id'), primary_key=True),
    db.Column('worker_id', db.Integer, db.ForeignKey(
        'worker.id'), primary_key=True),
)


class Worker(db.Model):
    __tablename__ = 'worker'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(128), nullable=True)

    worker_orders = db.relationship(
        'WorkOrder', secondary=work_order_workers, lazy='subquery',
        backref=db.backref('workers', lazy=True))

    def __repr__(self):
        ret = 'Worker ({}): {}\n'.format(self.id, self.name)
        orders_str = ""
        for order in self.worker_orders:
            orders_str += "* " + order.title + "\n"
        ret += orders_str
        return ret


class WorkOrder(db.Model):
    __tablename__ = 'work_order'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    deadline = db.Column(db.Date(), nullable=True)

    def __repr__(self):
        ret = 'WorkOrder ({}): {}\n'.format(self.id, self.title)
        workers_str = ""
        for worker in self.workers:
            workers_str += "- " + worker.name + "\n"
        ret += workers_str
        return ret
