import click
import os

@click.group()
def cli():
    pass

@cli.command()
def run_customers_api():
    from customers_api.app import run_app
    run_app()

@cli.command()
def run_invoices_api():
    from invoices_api.app import run_app
    run_app()

@cli.command()
def run_revenue_api():
    from revenue_api.app import run_app
    run_app()

@cli.command()
def run_users_api():
    from users_api.app import run_app
    run_app()

# For now it's done using requests
@cli.command()
def populatedb():
    from sample_data import (
        users,
        customers,
        invoices,
        revenue
    )
    import requests
    from dotenv import load_dotenv

    load_dotenv(override=True)

    customers_url = 'http://' + os.getenv('CUSTOMERS_API_HOST_URL', 'http://127.0.0.1') + ':' + str(os.getenv('CUSTOMERS_API_HOST_PORT', 8000))
    revenue_url = 'http://' + os.getenv('REVENUE_API_HOST_URL', 'http://127.0.0.1') + ':' + str(os.getenv('REVENUE_API_HOST_PORT', 8001))
    invoices_url = 'http://' + os.getenv('INVOICES_API_HOST_URL', 'http://127.0.0.1') + ':' + str(os.getenv('INVOICES_API_HOST_PORT', 8002))
    users_url = 'http://' + os.getenv('USERS_API_HOST_URL', 'http://127.0.0.1') + ':' + str(os.getenv('USERS_API_HOST_PORT', 8003))

    # Check that all APIs are online
    customers_resp = requests.get(customers_url + '/customers')
    revenue_resp = requests.get(revenue_url + '/revenue')
    invoices_resp = requests.get(invoices_url + '/invoices')
    users_resp = requests.get(users_url + '/users')

    if customers_resp.status_code != 200:
        click.echo(f'Something wrong with Customers API! Response {customers_resp.status_code}')
        return
    if revenue_resp.status_code != 200:
        click.echo(f'Something wrong with Revenue API! Response {revenue_resp.status_code}')
        return
    if invoices_resp.status_code != 200:
        click.echo(f'Something wrong with Invoices API! Response {invoices_resp.status_code}')
        return
    if users_resp.status_code != 200:
        click.echo(f'Something wrong with Users API! Response {invoices_resp.status_code}')

    click.echo('Populating users...')
    for user in users:
        user.pop('id')
        resp = requests.post(users_url + '/users', json=user)
        if resp.status_code != 201:
            click.echo(f'Something went wrong with Users API! Response {resp.status_code}')
            return

    click.echo('Populating customers...')
    customer_ids = []
    for customer in customers:
        customer.pop('id')
        resp = requests.post(customers_url + '/customers', json=customer)
        if resp.status_code != 201:
            click.echo(f'Something wrong with Customers API! Response {resp.status_code}')
            return
        customer_ids.append(resp.json()['id'])

    click.echo('Populating revenue...')
    for rev in revenue:
        resp = requests.post(revenue_url + '/revenue', json=rev)
        if resp.status_code != 201:
            click.echo(f'Something wrong with Revenue API! Response {resp.status_code}')
            return
        
    click.echo('Populating invoices...')
    for invoice in invoices:
        invoice['customer_id'] = customer_ids[invoice['customer_id']]
        resp = requests.post(invoices_url + '/invoices', json=invoice)
        if resp.status_code != 201:
            click.echo(f'Something wrong with Invoices API! Response {resp.status_code}')
            return
    
    click.echo('Done!')

@cli.command()
def initdb():
    click.echo('Began initializing db...')

    click.echo('CUSTOMERS API:')
    os.chdir('customers_api/')
    os.system('python -m alembic upgrade heads')

    click.echo('INVOICES API:')
    os.chdir('../invoices_api/')
    os.system('python -m alembic upgrade heads')

    click.echo('REVENUE API:')
    os.chdir('../revenue_api/')
    os.system('python -m alembic upgrade heads')

    click.echo('USERS API:')
    os.chdir('../users_api/')
    os.system('python -m alembic upgrade heads')

    click.echo('DONE')

@cli.command()
def dropdb():
    import requests
    from dotenv import load_dotenv

    load_dotenv(override=True)

    customers_url = 'http://' + os.getenv('CUSTOMERS_API_HOST_URL', 'http://127.0.0.1') + ':' + str(os.getenv('CUSTOMERS_API_HOST_PORT', 8000))
    revenue_url = 'http://' + os.getenv('REVENUE_API_HOST_URL', 'http://127.0.0.1') + ':' + str(os.getenv('REVENUE_API_HOST_PORT', 8001))
    invoices_url = 'http://' + os.getenv('INVOICES_API_HOST_URL', 'http://127.0.0.1') + ':' + str(os.getenv('INVOICES_API_HOST_PORT', 8002))
    users_url = 'http://' + os.getenv('USERS_API_HOST_URL', 'http://127.0.0.1') + ':' + str(os.getenv('USERS_API_HOST_PORT', 8003))

    # Check that all APIs are online
    customers_resp = requests.get(customers_url + '/customers')
    revenue_resp = requests.get(revenue_url + '/revenue')
    invoices_resp = requests.get(invoices_url + '/invoices')
    users_resp = requests.get(users_url + '/users')

    if customers_resp.status_code != 200:
        click.echo(f'Something wrong with Customers API! Response {customers_resp.status_code}')
        return
    if revenue_resp.status_code != 200:
        click.echo(f'Something wrong with Revenue API! Response {revenue_resp.status_code}')
        return
    if invoices_resp.status_code != 200:
        click.echo(f'Something wrong with Invoices API! Response {invoices_resp.status_code}')
        return
    if users_resp.status_code != 200:
        click.echo(f'Something wrong with Users API! Response {invoices_resp.status_code}')
    
    click.echo('Deleting users...')
    for user in users_resp.json():
        resp = requests.delete(users_url + '/users/' + user['email'])
        if resp.status_code != 204:
            click.echo(f'Something wrong with Users API! Response {resp.status_code}')
            return

    click.echo('Deleting customers...')
    for customer in customers_resp.json()['customers']:
        resp = requests.delete(customers_url + '/customers/' + customer['id'])
        if resp.status_code != 204:
            click.echo(f'Something wrong with Customers API! Response {resp.status_code}')
            return

    click.echo('Deleting revenue...')
    for rev in revenue_resp.json()['revenue']:
        resp = requests.delete(revenue_url + '/revenue/' + rev['month'])
        if resp.status_code != 204:
            click.echo(f'Something wrong with Revenue API! Response {resp.status_code}')
            return

    click.echo('Deleting invoices...')
    for invoice in invoices_resp.json()['invoices']:
        resp = requests.delete(invoices_url + '/invoices/' + str(invoice['id']))
        if resp.status_code != 204:
            click.echo(f'Something wrong with Invoices API! Response {resp.status_code}')
            return
        
    click.echo('Done!')

if __name__=='__main__':
    cli()
