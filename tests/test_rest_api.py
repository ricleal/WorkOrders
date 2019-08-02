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


def test_delete(app, fake):

    data = {
        "email": "ksanchez@yahoo.com",
        "name": "Chad Spears"
    }

    c = app.test_client()

    # Insert
    response = c.post('/worker', data=json.dumps(data),
                      content_type='application/json')
    response_data = response.data.decode('utf-8').strip()
    assert response.status_code == 201
    assert type(int(response_data)) ==  int

    response = c.get('/worker/{}'.format(response_data))
    print(response.data)
    assert response.status_code == 200
    d = _get_response_data_as_dict(response)
    assert d['name'] and d['email']

    response = c.delete('/worker/{}'.format(response_data),
                        content_type='application/json')
    print(response.data)
    assert response.status_code == 204
    assert '' == response.data.decode('utf-8')
