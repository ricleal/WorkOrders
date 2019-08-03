import sys
import json
import random
from datetime import datetime
from orders.model import Worker, WorkOrder


def _get_response_data_as_dict(response):
    return json.loads(response.data.decode('utf8'))


def _create_worker(db, fake):

    w = Worker(
        name=fake.name(),
        email=fake.email()
    )
    db.session.add(w)
    db.session.commit()
    return w


def _create_work_order(db, fake):

    wo = WorkOrder(
        title=fake.sentence(nb_words=random.randint(4, 10)),
        description=fake.text(max_nb_chars=random.randint(50, 100)),
        deadline=datetime.strptime(fake.date(), "%Y-%m-%d").date(),
    )
    db.session.add(wo)
    db.session.commit()
    return wo


def test_query(db, fake):

    worker_obj = _create_worker(db, fake)
    worker = Worker.query.get(worker_obj.id)
    assert worker.__dict__['name'] and worker.__dict__['email']


def test_worker(app, fake):
    '''
    For worker tests:
    Post/get/delete
    '''

    data = {
        "email": "ksanchez@yahoo.com",
        "name": "Chad Spears"
    }

    c = app.test_client()

    # Create
    response = c.post('/worker', data=json.dumps(data),
                      content_type='application/json')
    response_data = response.data.decode('utf-8').strip()
    assert response.status_code == 201
    assert type(int(response_data)) == int

    # create invalid data
    data.pop("email")
    data['X'] = 123
    response = c.post('/worker', data=json.dumps(data),
                      content_type='application/json')
    response_dic = _get_response_data_as_dict(response)
    assert response.status_code == 422
    assert "message" in response_dic.keys()

    # get
    response = c.get('/worker/{}'.format(response_data))
    assert response.status_code == 200
    d = _get_response_data_as_dict(response)
    assert d['name'] and d['email']

    # get invalid
    response = c.get('/worker/{}'.format(sys.maxsize))
    d = _get_response_data_as_dict(response)
    assert response.status_code == 404
    assert d["message"] == "Worker {} does not exist".format(sys.maxsize)

    # delete
    response = c.delete('/worker/{}'.format(response_data),
                        content_type='application/json')
    assert response.status_code == 204
    assert '' == response.data.decode('utf-8')

    # delete invalid
    response = c.delete('/worker/{}'.format(sys.maxsize),
                        content_type='application/json')
    d = _get_response_data_as_dict(response)
    assert response.status_code == 404
    assert d["message"] == "Worker {} does not exist".format(sys.maxsize)


def test_assign_worker_to_work_order(app, db, fake):

    # Test update
    # word_id / order_id
    c = app.test_client()
    workers = [_create_worker(db, fake) for _ in range(7)]
    work_order = _create_work_order(db, fake)

    # All OK
    for index, w in enumerate(workers):
        response = c.put('/worker/{}/workorder/{}'.format(w.id, work_order.id))
        if index < 5:
            assert response.status_code == 200
        else:
            # More than 5 workers assigned to this order
            assert response.status_code == 404


def test_work_order(app, db, fake):

    data = {
        "deadline": "2020-12-25",
        "title": "Team worker expect population hair occur same forward.",
        "description": "No pattern able. State parent where our avoid step."
    }

    c = app.test_client()

    # Create
    response = c.post('/workorder', data=json.dumps(data),
                      content_type='application/json')
    response_data = response.data.decode('utf-8').strip()
    assert response.status_code == 201
    assert type(int(response_data)) == int

    # Create invalid data
    data.pop('title')
    response = c.post('/workorder', data=json.dumps(data),
                      content_type='application/json')
    response_dic = _get_response_data_as_dict(response)
    assert response.status_code == 422
    assert "message" in response_dic.keys()

    # Get all orders
    response = c.get('/workorder')
    assert response.status_code == 200
    d = _get_response_data_as_dict(response)
    assert type(d) == list and len(d) == 1

    # Added 5 orders: Get all orders
    [_create_work_order(db, fake) for _ in range(5)]
    response = c.get('/workorder')
    assert response.status_code == 200
    response_list = _get_response_data_as_dict(response)
    assert type(response_list) == list and len(response_list) == 6
    # See if the dates are sorted!
    for i in range(len(response_list[:-1])):
        date1 = datetime.strptime(response_list[i]['deadline'], '%Y-%m-%d')
        date2 = datetime.strptime(response_list[i+1]['deadline'], '%Y-%m-%d')
        assert date2 < date1


def test_work_order_by_worker(app, db, fake):

    c = app.test_client()

    # Get and order for a worker:
    w = _create_worker(db, fake)
    wo = _create_work_order(db, fake)
    # Add the worker to the work order
    wo.workers.append(w)
    db.session.commit()
    # Now let's look for what we created
    response = c.get('/workorder/worker/{}'.format(w.id))
    assert response.status_code == 200
    response_json = _get_response_data_as_dict(response)
    for d in response_json:
        assert d['deadline'] and d['title'] and d['description']

    # Get and order for an invalid worker:
    response = c.get('/workorder/worker/{}'.format(sys.maxsize))
    assert response.status_code == 404
    d = _get_response_data_as_dict(response)
    assert d["message"] == "No Work Order exists for worker {}".format(
        sys.maxsize)
