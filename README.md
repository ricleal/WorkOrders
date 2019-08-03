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

# Production

`gunicorn -w 2 --bind 0.0.0.0:8000 run_prod:app`

