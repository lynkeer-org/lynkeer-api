from fastapi import FastAPI
from api.v1.routers import customers  # This should work if structure is correct

from models import Transaction, Invoice
from db import create_all_tables


app = FastAPI(
    lifespan=create_all_tables
)  # This is a FastAPI application instance. The lifespan parameter is used to create and drop the database tables when the application starts and stops.
app.include_router(customers.router)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):

    return transaction_data


@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):

    return invoice_data
