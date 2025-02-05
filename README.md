# Interview Scheduler
A basic interview scheduling application built with Python and FastAPI.

# Requirements
* Python 3.10 or higher
* PostgreSQL Database

# Installation and Setup
Step 1: Install Poetry
Poetry is used to manage dependencies and the virtual environment. Install it via pip:

```sh
$ pip install poetry
```
Step 2: Install Dependencies
After installing Poetry, install the required packages using the following command:

```sh
$ poetry install
```

Step 3: Activate Poetry Shell
Activate the virtual environment created by Poetry:

```sh
$ poetry shell
```
This will allow you to run the application with all the required dependencies.

Database Setup
This application uses PostgreSQL as its database. To ensure the application runs successfully, you will need to create the necessary tables. Please make sure the database is properly configured.

Running the Application
Once the environment is set up and the database is configured, you can run the FastAPI application using Uvicorn:


```sh
$ python main.py
```
main refers to your main application file.
app is the FastAPI instance in that file.
The server will start running on http://0.0.0.0:8420.

Notes
Ensure your PostgreSQL database is running and accessible by the application.
You may need to adjust your database settings and table creation queries based on your project structure.
