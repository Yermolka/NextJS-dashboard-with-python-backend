import { sql } from '@vercel/postgres';
import {
  CustomerField,
  CustomersTableType,
  InvoiceForm,
  InvoicesTable,
  LatestInvoiceRaw,
  User,
  Revenue,
  Customer,
  LatestInvoice,
  Invoice,
  FormattedCustomersTable,
} from './definitions';
import { formatCurrency } from './utils';
import { unstable_noStore } from 'next/cache';

export async function fetchRevenue() {
  unstable_noStore();
  try {
    const resp = await fetch(`${process.env.REVENUE_API_URL}/revenue`);
    if (resp.status != 200) {
      throw new Error(`Revenue API Error: GET /revenue ${resp.status}`);
    }

    const data: {revenue: Revenue[]} = await resp.json();
    return data.revenue;
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch revenue data.');
  }
  process.env.CUSTOMERS_API_URL;
}

export async function fetchLatestInvoices() {
  unstable_noStore();
  try {
    const resp = await fetch(`${process.env.INVOICES_API_URL}/invoices/latest`);
    if (resp.status != 200) {
      throw new Error(`Invoices API Error: GET /invoices/latest ${resp.status}`);
    }
    const latestInvoices: {invoices: LatestInvoice[]} = await resp.json();
    
    return latestInvoices.invoices;
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch the latest invoices.');
  }
}

export async function fetchCardData() {
  unstable_noStore();
  try {
    const resp = await Promise.all([
      fetch(`${process.env.CUSTOMERS_API_URL}/customers/count`),
      fetch(`${process.env.INVOICES_API_URL}/invoices/count`),
      fetch(`${process.env.INVOICES_API_URL}/invoices/total?status=paid`),
      fetch(`${process.env.INVOICES_API_URL}/invoices/total?status=pending`)
    ])

    resp.forEach((value) => {
      if (value.status != 200) {
        throw new Error(`API Error: ${value.url} ${value.status}`)
      }
    })

    const numberOfCustomers = (await resp[0].json() as {count: number}).count;
    const numberOfInvoices = (await resp[1].json() as {count: number}).count;
    const totalPaidInvoices = (await resp[2].json() as {total: number}).total / 100;
    const totalPendingInvoices = (await resp[3].json() as {total: number}).total / 100;

    return {
      numberOfCustomers,
      numberOfInvoices,
      totalPaidInvoices,
      totalPendingInvoices,
    };
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch card data.');
  }
}

const ITEMS_PER_PAGE = 6;
export async function fetchFilteredInvoices(
  query: string,
  currentPage: number,
) {
  unstable_noStore()
  const offset = (currentPage - 1) * ITEMS_PER_PAGE;

  try {
    const resp = await fetch(`${process.env.INVOICES_API_URL}/invoices/filtered?query=${query}&currentPage=${currentPage}`);
    if (resp.status != 200) {
      throw new Error(`Invoices API Error: GET /invoices/filtered?query=${query}&currentPage=${currentPage} ${resp.status}`);
    }

    const invoices: {invoices: LatestInvoice[]} = await resp.json();
    return invoices.invoices;
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch invoices.');
  }
}

export async function fetchInvoicesPages(query: string) {
  unstable_noStore()
  try {
  //   const count = await sql`SELECT COUNT(*)
  //   FROM invoices
  //   JOIN customers ON invoices.customer_id = customers.id
  //   WHERE
  //     customers.name ILIKE ${`%${query}%`} OR
  //     customers.email ILIKE ${`%${query}%`} OR
  //     invoices.amount::text ILIKE ${`%${query}%`} OR
  //     invoices.date::text ILIKE ${`%${query}%`} OR
  //     invoices.status ILIKE ${`%${query}%`}
  // `;

  //   const totalPages = Math.ceil(Number(count.rows[0].count) / ITEMS_PER_PAGE);
    
    
    return 5;
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch total number of invoices.');
  }
}

export async function fetchInvoiceById(id: string) {
  unstable_noStore()
  try {
    const resp = await fetch(`${process.env.INVOICES_API_URL}/invoices/${id}`);
    if (resp.status === 404) {
      return null
    } else if (resp.status != 200) {
      throw new Error(`Invoice API Error: GET /invoices/${id} ${resp.status}`);
    }
    const data = await resp.json() as Invoice;
    data.amount /= 100;
    return data;
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch invoice.');
  }
}

export async function fetchCustomers() {
  unstable_noStore()
  try {
    const resp = await fetch(`${process.env.CUSTOMERS_API_URL}/customers`);
    if (resp.status != 200) {
      throw new Error(`Customers API Error: GET /customers ${resp.status}`)
    }

    const data: {customers: Customer[]} = await resp.json();
    return data.customers;
  } catch (err) {
    console.error('Database Error:', err);
    throw new Error('Failed to fetch all customers.');
  }
}

export async function fetchFilteredCustomers(query: string) {
  unstable_noStore()
  try {
    const resp = await fetch(`${process.env.CUSTOMERS_API_URL}/customers/filtered?query=${query}`)
    if (resp.status != 200) {
      throw new Error('Customers API Error')
    }
    const data: { customers: FormattedCustomersTable[] }= await resp.json();
    return data.customers;
  } catch (err) {
    console.error('Database Error:', err);
    throw new Error('Failed to fetch customer table.');
  }
}

export async function getUser(email: string) {
  unstable_noStore()
  try {
    const user = await sql`SELECT * FROM users WHERE email=${email}`;
    return user.rows[0] as User;
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw new Error('Failed to fetch user.');
  }
}
