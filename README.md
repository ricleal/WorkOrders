# Introduction

Back-end of a RESTFul app that has work orders and workers.
A work order is a job to be completed by one or more workers
(up to 5 workers can work on the same order)

The worker has the following information:
- The worker name
- Company name
- Email

The work order has:
- Title
- Description
- A Deadline to be completed


# Installation

It's better to use a virtual environment to deploy the app locally.

```
virtualenv venv -p python3

source venv/bin/activate
```

Install the requirements:
```
pip install -r requirements.txt
```

Create an `.env` file. See `env.base` for a template.
If the file / environment variable does not exist, the default argument of `os.getenv`
is used. See `orders/config.py` for more details.


Fire up the app in development:
```
python run_dev.py
```
To test: http://localhost:5000/workorder

In production:
```
gunicorn -w <number of workers> --bind <IP>:<port> run_prod:app

# E.g.:
gunicorn -w 2 --bind 0.0.0.0:8000 run_prod:app
```
To test: https:// 0.0.0.0:8000/api/v1/workorder

Note that in production, the end points are prefixed with: `/api/v1`


# App functionality

## Create a worker

- HTTP Method: `POST`
- End point: `/worker`
- JSON example:
```json
{
    "name": "Chad Spears",
    "company": "Soft skills LLC",
    "email": "ksanchez@yahoo.com"
}
```
- HTTP Success Response:
    - Code: 201
    - Data: The primary key (id) of the worker created

## Delete a worker

- HTTP Method: `DELETE`
- End point: `/worker/<int:worker_id>`
- HTTP Success Response:
    - Code: 204

## Create a work order

Note that there are no workers assigned yet to the work order.

- HTTP Method: `POST`
- End point: `/workorder`
- JSON example:
```json
{
    "title": "Team worker expect population hair occur same forward.",
    "description": "No pattern able. State parent where our avoid step.",
    "deadline": "2020-12-25"
}
```
- HTTP Success Response:
    - Code: 201
    - Data: The primary key (id) of the work order created

## Assigning a worker to an order

- HTTP Method: `PUT`
- End point: `/worker/<int:worker_id>/workorder/<int:work_order_id>`
- HTTP Success Response:
    - Code: 200

## Fetch all work orders for a specific worker

- HTTP Method: `GET`
- End point: `/workorder/worker/<int:worker_id>`
- HTTP Success Response:
    - Code: 200
    - Data: the requested info, e.g.:
```json
[
    {
        "id": 1,
        "title": "To student analysis recently night less yes sea.",
        "description": "Since player president economy. (...)",
        "deadline": "1971-07-10",
        "workers": [
            {
                "name": "Jessica Moore",
                "email": "kayleewashington@gmail.com",
                "id": 1,
                "company": "Jones LLC",
                "worker_orders": [
                    1,
                    2
                ]
            },
            {
                "name": "Susan Long",
                "email": "levimoreno@hotmail.com",
                "id": 2,
                "company": "Hammond-Kim",
                "worker_orders": [
                    1
                ]
            }
        ]
    },
    {
        "id": 2,
        "title": "Evening recently time themselves treat.",
        "description": "Call spring system show which property on. (...)",
        "deadline": "2001-06-19",
        "workers": [
            {
                "name": "Jessica Moore",
                "email": "kayleewashington@gmail.com",
                "id": 1,
                "company": "Jones LLC",
                "worker_orders": [
                    1,
                    2
                ]
            }
        ]
    }
]
```


## Fetch all work orders sorted by deadline

- HTTP Method: `GET`
- End point: `/workorder`
- HTTP Success Response:
    - Code: 200
    - Data: the requested info, e.g.:
```json
[
    {
        "id": 4,
        "title": "Team worker expect population hair occur same forward.",
        "description": "No pattern able. State parent where our avoid step.",
        "deadline": "2020-12-25",
        "workers": []
    },
    {
        "id": 9,
        "title": "Team worker expect population hair occur same forward.",
        "description": "No pattern able. State parent where our avoid step.",
        "deadline": "2019-12-25",
        "workers": []
    },
    {
        "id": 14,
        "title": "Team worker expect population hair occur same forward.",
        "description": "No pattern able. State parent where our avoid step.",
        "deadline": "2018-10-22",
        "workers": []
    }
]
```

# Run the tests

One can run the tests using `pytest`. First install it:
```
pip install -r requirements_test.txt
```

Than run it calling `pytest`. 
The output should be similar to the following:
```
$ pytest -v
================================================================================ test session starts =================================================================================
platform darwin -- Python 3.7.3, pytest-5.0.1, py-1.8.0, pluggy-0.12.0 -- /Users/rhf/git/WorkOrders/venv/bin/python3.7
cachedir: .pytest_cache
rootdir: /Users/rhf/git/WorkOrders
collected 6 items

tests/test_model.py::test_creation PASSED                                                                                                                                      [ 16%]
tests/test_rest_api.py::test_query PASSED                                                                                                                                      [ 33%]
tests/test_rest_api.py::test_worker PASSED                                                                                                                                     [ 50%]
tests/test_rest_api.py::test_assign_worker_to_work_order PASSED                                                                                                                [ 66%]
tests/test_rest_api.py::test_work_order PASSED                                                                                                                                 [ 83%]
tests/test_rest_api.py::test_work_order_by_worker PASSED                                                                                                                       [100%]

============================================================================== 6 passed in 0.49 seconds ==============================================================================
```




# Bonus: Install it in Heroku

This is assumed that you:
- Have an account in Heroku
- Have an SSH key inside
- Have installed locally the `heroku` application.

Create a file `Procfile` if it does not exist.
Write in this file:
```
web: gunicorn run_prod:app
```

Then do:
```
git push heroku master
```

If the app does not start:
```
heroku ps:scale web=1
```

To open a browser window:
```
heroku open
```

To see the logs:
```
heroku logs --tail
```

