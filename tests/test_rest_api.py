import json

import pytest
from orders import db

from orders.model import Worker


def _get_response_data_as_dict(response):
    return json.loads(response.data.decode('utf8'))


def _create_worker(fake):

    w = Worker(
        name=fake.name(),
        email=fake.email()
    )
    db.session.add(w)
    db.session.commit()
    return w


def test_delete(app, fake):

    worker_obj = _create_worker(fake)
    print("\n****", worker_obj.id)
    worker = Worker.query.get(worker_obj.id)
    print("+++++++++++++", worker)

    data = {
        "email": "ksanchez@yahoo.com",
        "name": "Chad Spears",
    }

    with app.test_client() as c:

        # Insert
        response = c.post('/worker', data=json.dumps(data),
                          content_type='application/json')
        print(response.data)
        assert response.status_code == 201
        assert 'inserted_id' in _get_response_data_as_dict(response).keys()

        response = c.get('/worker/1')
        print(response.data)
        assert response.status_code == 200
        assert '' == response.data.decode('utf-8')

        response = c.delete('/worker/1',
                            content_type='application/json')
        print(response.data)
        assert response.status_code == 204
        assert '' == response.data.decode('utf-8')
