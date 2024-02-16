# Fullstack app based on NextJS official tutorial

## Prerequisites
For frontend:

NodeJS>=18.17.x
> cd nextjs-dashboard
>
> npm install --dev

For backend

Python>=3.12
> cd python-backend

With pip:
> pip install -r requirements.txt

or with pipenv:
> pip install pipenv
>
> pipenv shell
>
> pipenv install


## How to run
### Backend
Create a .env file, fill it from .env.example

> python utility.py initdb
> 
> python utility.py run-customers-api
>
> python utility.py run-invoices-api
>
> python utility.py run-revenue-api
>
> python utility.py run-users-api
>
> python utility.py populatedb

### Frontend
Create a .env file, fill it from .env.example

> npm run dev

This would start a server at localhost:3000 by default. Sample user for logging in is email: user@nextmail.ru, pwd: 123456
