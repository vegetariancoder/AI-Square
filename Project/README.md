# FastAPI Practice Project: Personal Expense Tracker API

## Project Idea

Build a **Personal Expense Tracker API** using FastAPI.

This project will help you practice the same concepts used in your Udemy Todo application, but with a new real-world use case. Instead of managing todos, users will register, log in, and manage their own expenses.

Each user should only be able to view, create, update, and delete their own expenses.

## Concepts You Will Practice

- FastAPI application setup
- Routers for separating features
- Pydantic models for request validation
- SQLAlchemy models for database tables
- MySQL database connection
- Dependency injection using `Depends`
- Database session dependency
- Password hashing with `passlib`
- Login using OAuth2 password form
- JWT access token creation
- Protected routes using the current logged-in user
- CRUD operations
- Path parameters and validation
- HTTP status codes and exceptions
- Swagger UI testing

## Application Features

Your API should support these features:

- Register a new user
- Log in with username and password
- Generate a JWT access token
- Get current user's profile
- Add a new expense
- Get all expenses for the logged-in user
- Get one expense by ID
- Update an expense
- Delete an expense
- Filter expenses by category
- Mark an expense as recurring or non-recurring

## Example Expense Data

An expense can have:

- `title`: Grocery shopping
- `description`: Bought vegetables and snacks
- `amount`: 45.50
- `category`: Food
- `payment_method`: Credit Card
- `is_recurring`: false
- `owner_id`: ID of the user who created the expense

## Suggested Project Structure

Create this structure inside:

```text
/Users/sahilnagpal/Desktop/AI-Square/Project/Expense_Tracker_API/
```

Recommended files:

```text
Expense_Tracker_API/
├── main.py
├── database.py
├── models.py
├── requirements.txt
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   ├── users.py
│   └── expenses.py
└── README.md
```

## Step-by-Step Build Plan

### Step 1: Create the Project Folder

Create a new folder:

```bash
mkdir -p /Users/sahilnagpal/Desktop/AI-Square/Project/Expense_Tracker_API/routers
```

Then create these files:

```text
main.py
database.py
models.py
requirements.txt
routers/__init__.py
routers/auth.py
routers/users.py
routers/expenses.py
```

## Step 2: Create `requirements.txt`

Add the packages you need:

```text
fastapi
uvicorn
sqlalchemy
pymysql
passlib[bcrypt]
python-jose[cryptography]
python-multipart
typing-extensions
```

Install them:

```bash
pip install -r requirements.txt
```

## Step 3: Create the MySQL Database

Open MySQL and create a database:

```sql
CREATE DATABASE expense_tracker_db;
```

You will connect FastAPI to this database from `database.py`.

## Step 4: Build `database.py`

Use this file for:

- Database URL
- SQLAlchemy engine
- SessionLocal
- Base
- `get_db()` dependency

Your database URL will look similar to:

```python
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/expense_tracker_db"
```

Change `root`, `password`, host, port, or database name based on your local MySQL setup.

## Step 5: Build `models.py`

Create two SQLAlchemy models:

### `Users` Table

Fields:

- `id`
- `email`
- `username`
- `first_name`
- `last_name`
- `password`
- `is_active`
- `role`

### `Expense` Table

Fields:

- `id`
- `title`
- `description`
- `amount`
- `category`
- `payment_method`
- `is_recurring`
- `owner_id`

The `owner_id` field should be a foreign key connected to the `users.id` column.

## Step 6: Build `main.py`

In `main.py`, you should:

- Create the FastAPI app
- Add title, description, and version
- Create database tables using `models.Base.metadata.create_all(bind=engine)`
- Include routers for auth, users, and expenses
- Start the app with Uvicorn

Example API title:

```python
app = FastAPI(
    title="Personal Expense Tracker API",
    description="API for tracking personal expenses with login and JWT authentication.",
    version="1.0.0"
)
```

## Step 7: Build `routers/users.py`

Use this router for user registration and user information.

Create a Pydantic model called `UserRequest`.

Fields:

- `email`
- `username`
- `first_name`
- `last_name`
- `password`
- `is_active`
- `role`

Endpoints to build:

```text
POST /add_user
GET /all_users_info
```

Important:

- Hash the password before saving the user.
- Use `bcrypt_context.hash(user_request.password)`.
- Do not store plain text passwords.

## Step 8: Build `routers/auth.py`

Use this router for login and JWT authentication.

Functions to create:

- `authenticate_user(username, password, db)`
- `create_access_token(username, user_id, expires_delta)`
- `get_current_user(token)`

Endpoint to build:

```text
POST /token
```

This endpoint should:

- Accept username and password using `OAuth2PasswordRequestForm`
- Check if the user exists
- Verify the password
- Return a JWT token

Example response:

```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

## Step 9: Build `routers/expenses.py`

Use this router for expense CRUD operations.

Create a Pydantic model called `ExpenseRequest`.

Fields:

- `title`
- `description`
- `amount`
- `category`
- `payment_method`
- `is_recurring`
- `owner_id`

Endpoints to build:

```text
GET /expenses
GET /expenses/{expense_id}
POST /add_expense
PUT /expenses/{expense_id}
DELETE /expenses/{expense_id}
GET /expenses/category/{category_name}
```

Important rules:

- All expense endpoints should require login.
- Use `get_current_user` as a dependency.
- When reading expenses, only return expenses where `Expense.owner_id == user.get("id")`.
- When updating or deleting an expense, check that the expense belongs to the logged-in user.

## Step 10: Run the Application

From the project folder, run:

```bash
uvicorn main:app --reload
```

Then open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Step 11: Test the API in Swagger UI

Follow this order:

1. Create a user using `POST /add_user`.
2. Log in using `POST /token`.
3. Copy the returned access token.
4. Click the `Authorize` button in Swagger UI.
5. Enter the token using this format:

```text
Bearer your_token_here
```

6. Create an expense using `POST /add_expense`.
7. Get all expenses using `GET /expenses`.
8. Get one expense using `GET /expenses/{expense_id}`.
9. Update an expense using `PUT /expenses/{expense_id}`.
10. Delete an expense using `DELETE /expenses/{expense_id}`.

## Step 12: Suggested Validation Rules

Use Pydantic `Field` validation.

Examples:

- `title` should have minimum length 1 and maximum length 100.
- `description` should have maximum length 255.
- `amount` should be greater than 0.
- `category` should have minimum length 1.
- `payment_method` should have minimum length 1.

Example:

```python
amount: float = Field(gt=0, description="Expense amount must be greater than 0")
```

## Step 13: Suggested Categories

You can use categories like:

- Food
- Travel
- Shopping
- Bills
- Rent
- Health
- Education
- Entertainment
- Other

## Step 14: Extra Practice Features

After completing the basic version, add these features:

- Get total expense amount for logged-in user
- Get expenses greater than a given amount
- Get expenses by payment method
- Add created date to each expense
- Add monthly expense summary
- Add admin-only endpoint to view all users' expenses
- Add role-based access control using the `role` field

## Recommended Learning Order

Build the project in this order:

1. `database.py`
2. `models.py`
3. `main.py`
4. `routers/users.py`
5. `routers/auth.py`
6. `routers/expenses.py`
7. Test with Swagger UI
8. Add extra features

## Final Goal

By the end of this project, you should understand how to build a FastAPI backend where:

- Users can register and log in.
- Passwords are securely hashed.
- JWT tokens protect private endpoints.
- SQLAlchemy connects FastAPI to MySQL.
- Each user can only manage their own data.
- Routers keep the application organized.

This project is close enough to your Todo application to reuse the same concepts, but different enough that you will need to think and write the code yourself.
