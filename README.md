# imageRepositoryFlask

Image Flask Repository is a microservice restful api where people can create accounts, upload and store images, create albums. People cannot access other's images or albums. It uses JWT authentication currently. The database stores JWT token and keeps track of blacklisted tokens and expired tokens, albums and images. It has examples of one to one, one to many, and many to many relationships. Images are stored on the disc, while the location is stored in the database. Images are stored with guid, passwords are hashed before storing in database.

Production like setup uses Gunicorn as the WSGI interface for flask and Nginx as the web server for the web application.

Database used is Postgresql for both production and development setup.


<img src="https://i.morioh.com/fb42517ac4.png" width=400><img src="https://upload.wikimedia.org/wikipedia/commons/2/29/Postgresql_elephant.svg" width=200><img src="https://www.docker.com/sites/default/files/d8/2019-07/vertical-logo-monochromatic.png" width=200><img src="https://www.nginx.com/wp-content/uploads/2018/08/NGINX-logo-rgb-large.png" width=400><img src="https://www.fullstackpython.com/img/logos/gunicorn.jpg" width=600>

To deploy to development run the following
```
docker-compose up -d --build
```
and go to http://localhost:5000 and hit one of the endpoints

To run tests in development run the following
```
docker-compose exec web python manage.py seed_db
docker-compose exec web python manage.py run_tests
```
To deploy with nginx and gunicorn run the following
```
docker-compose -f docker-compose.prod.yaml up -d --build
docker-compose exec web python manage.py create_db
```
and go to http://localhost:1337 and hit one of the endpoints

TODO's when I get time
- Add react frontend and update docker containers
- Add JWT double submit authentication for protection as currently there is no way to authenticate that the JWT is being used by the user. NOTE will require creating unique json objects for flask-restful as it does not work with flask jsonify, Flask-restful json is based off of python json library and not flask json
