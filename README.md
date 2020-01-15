# imageRepositoryFlask

Image Flask Repository is a microservice restful api where people can create accounts, upload and store images, create albums. People cannot access other's images or albums. It uses JWT authentication currently. The database stores JWT token and keeps track of blacklisted tokens and expired tokens, albums and images. It has examples of one to one, one to many, and many to many relationships. Images are stored on the disc, while the location is stored in the database.
