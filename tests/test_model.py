import random
from datetime import datetime

from orders import db


def test_creation(app, fake):
    from orders.model import Worker, WorkOrder

    w1 = Worker(
        name=fake.name(),
        company=fake.company(),
        email=fake.email()
    )

    wo1 = WorkOrder(
        title=fake.sentence(nb_words=random.randint(4, 10)),
        description=fake.text(max_nb_chars=random.randint(100, 1000)),
        deadline=datetime.strptime(fake.date(), "%Y-%m-%d").date(),
    )

    wo2 = WorkOrder(
        title=fake.sentence(nb_words=random.randint(4, 10)),
        deadline=datetime.strptime(fake.date(), "%Y-%m-%d").date(),
    )

    w1.worker_orders.append(wo1)
    w1.worker_orders.append(wo2)
    db.session.add_all([w1, wo2, wo2])

    w2 = Worker(
        name=fake.name(),
        company=fake.company(),
        email=fake.email()
    )
    db.session.add(w2)

    wo1.workers.append(w2)

    db.session.flush()
    db.session.commit()

    assert db.session.query(Worker).filter(Worker.id == w1.id).count() == 1
    assert db.session.query(Worker).join(
        Worker.worker_orders).filter(Worker.id == w1.id).count() == 2
