import json

import pytest

from orders.model import Worker


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
    assert "message" in response_dic.keys()

    # get
    response = c.get('/worker/{}'.format(response_data))
    assert response.status_code == 200
    d = _get_response_data_as_dict(response)
    assert d['name'] and d['email']

    # delete
    response = c.delete('/worker/{}'.format(response_data),
                        content_type='application/json')
    assert response.status_code == 204
    assert '' == response.data.decode('utf-8')


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

    # Get all orders
    response = c.get('/workorder')
    assert response.status_code == 200
    d = _get_response_data_as_dict(response)
    assert type(d) == list and len(d) > 0

    # Get and order:
    response = c.get('/workorder/2')
    # response = c.get('/workorder/{}'.format(response_data))
    assert response.status_code == 200
    response_json = _get_response_data_as_dict(response)
    for d in response_json:
        assert d['deadline'] and d['title'] and d['description']

    # Test update
    # word_id / order_id
    workers = [_create_worker(db, fake) for _ in range(7)]
    for index, w in enumerate(workers):
        response = c.put('/worker/{}/{}'.format(w.id, 2))
        if index < 4:
            assert response.status_code == 200
        else:
            # More than 5 workers assigned to this order
            assert response.status_code == 404
