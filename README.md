# imageRepositoryFlask

Image Flask Repository is a microservice restful api where people can create accounts, upload and store images, create albums. People cannot access other's images or albums. It uses JWT authentication currently. The database stores JWT token and keeps track of blacklisted tokens and expired tokens, albums and images. It has examples of one to one, one to many, and many to many relationships. Images are stored on the disc, while the location is stored in the database. Images are stored with guid, passwords are hashed before storing in database.

Production like setup uses Gunicorn as the WSGI interface for flask and Nginx as the web server for the web application.

Database used is Postgresql for both production and development setup.
