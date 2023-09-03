# beyondcc assignment

## Description

This is a REST API resembling a movie database same as IMDb. The data about the movies is stored in a sqlite database that is already present in this repository under **/api/database/db.sqlite3**. This database is already populated with the data that was provided. But the code can generate a new sqlite database, on running the code if the database doesn't already exist. The repository also includes the SQL statments necessary to populate the database, which is present here **/sql/movie_data.sql**. The database schema includes *users*, *movies* and *genres* tables. The venv contains the necessary packages needed to run the folder. The API is documented with Swagger. The API uses ***JWT authentication*** for user authenication. 

**Packages used for this project**
- Flask
- Flask-RESTx
- Flask-SQLAlchemy
- Flask-JWT-Extended
- PyJWT
- python-dotenv

## API endpoints

- `POST /auth/signup`  
- `POST /auth/login`  
- `POST /auth/refresh` 🔒 
- `GET /movies/allmovies`
- `POST /movies/movie` 🔒 
- `PUT /movies/movie/{movie_id}` 🔒 
- `GET /movies/movie/{movie_id}` 🔒 
- `DELETE /movies/movie/{movie_id}` 🔒 

## To run the code

1. Clone the repo <br>
    `git clone https://github.com/Anu-Ra-g/beyondcc.git` <br>
2. Change the app directory <br>
    `cd beyondcc` 
3. Activate the virtual environment <br>
    `venv\Scripts\activate (Windows)` <br>
4. Run the command <br>
    `python runserver.py`

Activating the virtual environment, will make the app run with all the necessary packages. On, running the command, the development server will be activated, running at `localhost:5000`. The URL will present an UI, made with the help of Swagger UI. Here you can make the HTTP requests to the endpoints. 

![alt text for image](/Swagger.png)






