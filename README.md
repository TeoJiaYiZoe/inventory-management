# Inventory Management System

An inventory management system that perform CRU operations (create, read, update) on the inventory data.

## Table of Contents

- [API Endpoints](#api-endpoints)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Backend](#backend)
  - [Frontend](#frontend)
  - [Infrastructure (Terraform)](#infrastructure-terraform)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Cleanup](#clean-up)

## API Endpoints

| Endpoint                 | Method | Description              | Parameters (Type)                                                                                    |
| ------------------------ | ------ | ------------------------ | ---------------------------------------------------------------------------------------------------- |
| `/items/`                | POST   | Create or update item    | **Body**: `name` (str), `category` (str), `price` (float) – via `ItemCreate` model                   |
| `/items/{item_id}/price` | PUT    | Update item price        | **Path**: `item_id` (str) <br> **Body**: `price` (float) – via `PriceUpdate` model                   |
| `/items/`                | GET    | Query items by filters   | **Query**: `category` (str, optional), `dt_from` (str, optional), `dt_to` (str, optional)            |
| `/query-items/`          | GET    | Paginated/sorted results | **Query**: `name`, `category`, `price_min`, `price_max`, `page`, `limit`, `sort_field`, `sort_order` |

## Prerequisites

Before you begin, ensure you have the following installed:

- Docker (running)
- Python 3.7+
- Node.js and npm
- AWS CLI with configured credentials
- Terraform

## Setup

### Backend

1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   venv/Scripts/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start DynamoDB Local (Local testing)

   ```bash
   docker run -d -p 8000:8000 --name dynamodb amazon/dynamodb-local

   ```

### Frontend

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

### Infrastructure (Terraform)

**Note**: If you're only testing locally, you can skip the Terraform setup and use DynamoDB Local.

1. Initialize and apply infrastructure:
   ```bash
   cd backend/terraform
   terraform init
   terraform plan
   terraform apply
   ```

## Running the Application

### Start backend server

```bash
   cd backend
   uvicorn main:app --reload --host localhost --port 8001
```

### Start frontend development server

```bash
   cd frontend
   npm start
```

## Testing

### Run all tests

```bash
   cd backend
   pytest test
```

### Run specific file

```bash
   cd backend/test
   pytest test_validation.py
```

## Clean up

1. Stop backend server: Ctrl+C
2. Stop frontend server: Ctrl+C
3. Stop DynamoDB container
   `docker stop [container_id]`
4. Destroy Terraform resources (when needed)
   ```bash
   cd backend/terraform
   terraform destroy
   ```
