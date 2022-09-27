# Dockerized Postgres-Python demo

This is a demo on connecting to a postgres database from python.
I created the demo while learning on postgres, docker networking and connecting to a postgres db from a python application. Both the postgres db and the python application are set up in containers.

> Note: The postgres db is set up inside a container for convenience. This is not recommended for production use.

The repository contains two alternative ways for setting up the demo:

## 1. Using docker bridge network

Docker bridge networks allow isolated communication between containers running on the same docker daemon. It is easy to set up, as you can just refer to container names in place of host adress. However, because a postgres db would be unlikely to be be set inside a container in a realistic scenario, this is more of a demo of the bridge networks than the database connection. 

The setup is defined in `compose-bridge.yml`.

> Note: In this demo I'm passing the secrets as arguments to docker-compose. In a real project, use secret management tool such as docker secrets instead.

To run the demo:

(in terminal 1)

```console
$ POSTGRES_DB=postgres POSTGRES_USER=postgres POSTGRES_PASSWORD=postgres docker-compose -f compose-bridge.yml build

$ POSTGRES_DB=postgres POSTGRES_USER=postgres POSTGRES_PASSWORD=postgres docker-compose -f compose-bridge.yml up
```

Now there may be a couple of failed database connection attempts while the containers are set up, but finally you should get the following message:

```console
postgres-db-client  | Connection established to:  ('PostgreSQL 14.1 on aarch64-unknown-linux-musl, compiled by gcc (Alpine 10.3.1_git20211027) 10.3.1 20211027, 64-bit',)
```

(in terminal 2)

To shut down the containers and remove volumes:

```console
$ docker-compose -f compose-bridge.yml down -v
```

## 2. Using host network

Containers can also be mapped to the host network. Here the database connection is established through the local machine localhost public ip. Similar setup would also allow connecting from another machine over a network, but this runs both processes on the same machine for simpilicy. You can try establishing the connection while running the containers on separate machines as an exercise.

The difference to using bridge network is, that we map the containers to localhost ports and have to pass the localhost public ip as the host adress to the python app. The localhost public ip is retrieved with command:
```console
$ ifconfig -u | grep 'inet ' | grep -v 127.0.0.1 | cut -d\  -f2 | head -1
```

The setup is defined in `compose-host.yml`.

(in terminal 1)

```console
$ POSTGRES_DB=postgres POSTGRES_USER=postgres POSTGRES_PASSWORD=postgres POSTGRES_HOST=$(ifconfig -u | grep 'inet ' | grep -v 127.0.0.1 | cut -d\  -f2 | head -1) docker-compose -f compose-host.yml build

$ POSTGRES_DB=postgres POSTGRES_USER=postgres POSTGRES_PASSWORD=postgres POSTGRES_HOST=$(ifconfig -u | grep 'inet ' | grep -v 127.0.0.1 | cut -d\  -f2 | head -1) docker-compose -f compose-host.yml up
```

Again, you should get the same message of established connection as before.

(in terminal 2)

To shut down the containers and remove volumes:
```console
$ docker-compose -f compose-host.yml down -v
```

## References

In addition to Docker [compose](https://docs.docker.com/compose/compose-file/compose-file-v3/) and [networking](https://docs.docker.com/compose/networking/) documentation, and [psycopg tutorial](https://www.tutorialspoint.com/python_data_access/python_postgresql_database_connection.htm) I found [this blog post](https://geshan.com.np/blog/2021/12/docker-postgres/) by Geshan Manandhar the most useful while setting up this demo.
