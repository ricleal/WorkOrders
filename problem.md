# Backend Assessment - Work Orders

The goal is to build a small RESTful API that performs CRUD operations. Feel free to use
any language or framework you like. This assessment will be evaluated based on the
following criteria:
- Completion: Did you complete all the requirements? This is the most important
criterion.
- Fundamentals: How well is the data structured and how efficient is the code?
- Code Organization and Quality: How organized is your solution?
- Testing: Did you write some tests for the solution? How is the coverage?
- Communication: We are looking for candidates with strong communication
skills. This will be evaluated based on your Readme.md file.

## App

You are building the back-end of an app that has work orders and workers. A work order
is a job to be completed by one or more workers. Structure your application as you
would for any production app - include applicable classes, routes, persistent storage,
etc.

## Data Model

You can use any type of database you would like to store the data for this app. The
following basic information should be stored:
Worker
- Name (String)
- Company Name (String)
- Email (String)
Work Order
- Title (String)
- Description (String)
- Deadline (date)
One or more workers are ‘assigned’ to an order. A max of 5 workers can work on one
order.


## API

The application needs to have the following routes:
- Create a worker
- Delete a worker
- Create a work order
- Assigning a worker to an order
- Fetch all work orders:
  - For a specific worker
  - Sorted by deadline

