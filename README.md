backend_store_online
This README provides instructions to test registration, login, and GraphQL queries for the Django backend system implemented with Chokidar and Strawberry GraphQL.

Prerequisites
Install dependencies and ensure your project is set up correctly.
Verify that your Django server is ready and PostgreSQL is configured for custom user tables.
Testing Registration and Login
Follow these steps to test user registration and login functionalities using GraphQL. A GraphQL client like Postman, Insomnia, or GraphiQL can be used.

Step 1: Start Django Server
Run the following command to start the Django development server:

bash

python manage.py runserver
The server will be accessible at http://127.0.0.1:8000/graphql/ (or your configured endpoint).

Step 2: Registration
To register a new user, execute the following steps:

Open your GraphQL client (e.g., Postman, Insomnia, or GraphiQL).
Perform the following GraphQL mutation to register a user:
graphql

mutation {
register(
username: "testuser"
email: "testuser@example.com"
password: "securepassword"
name: "Test User"
avatar: "path/to/avatar.jpg"
) {
message
success
}
}
Expected Response: Successful registration will return:
json

{
"data": {
"register": {
"message": "User testuser registered successfully!",
"success": true
}
}
}
If the username or email is already taken, you will get an error response:

json

{
"data": {
"register": {
"message": "A user with that username or email already exists.",
"success": false
}
}
}
Step 3: Login
To log in with the registered user credentials, follow these steps:

Use the following login mutation:
graphql

mutation {
login(email: "testuser@example.com", password: "securepassword")
}
Expected Response: Successful login will return:
json

{
"data": {
"login": true
}
}
If the email or password is invalid, an exception will be raised:

json

{
"errors": [
{
"message": "Invalid username or password",
"locations": [{ "line": 2, "column": 3 }],
"path": ["login"]
}
]
}
GraphQL Product Queries
This section provides detailed queries for fetching:

Categories
Products
Single specific entries for categories or products.
Navigate to the GraphQL endpoint (http://127.0.0.1:8000/graphql/) to execute these queries.
Query: Fetch All Categories and Their Products
graphql

query {
allCategories {
id
name
description
products {
id
name
price
stock
}
}
}
Query: Fetch a Single Category by ID
graphql

query {
category(id: 1) {
id
name
description
products {
id
name
}
}
}
Query: Fetch All Products
graphql

query {
allProducts {
id
name
price
stock
category {
id
name
}
}
}
Query: Fetch a Single Product by ID
graphql

query {
product(id: 1) {
id
name
description
price
stock
category {
id
name
}
}
}
Protected Queries (Required Authentication)
After logging in successfully, you can access authenticated data by sending specific queries to the server. For example:

graphql

query {
protectedData
}
