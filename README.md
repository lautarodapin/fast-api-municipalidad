
.. code-block: sh

    heroku container:push web -a <app name>
    heroku container:release web -a <app name>  

[Heroku API link](https://fast-api-municipalidad.herokuapp.com/docs)


# AWS
En la consola de Linux
.. code-block: sh

    chmod 400 <PRIVATE_KEY_FILE_NAME>
    ssh -i <PRIVATE_KEY_FILE_NAME> ec2-user@<PUBLIC_DNS>
    docker run -d -p 8000:8000 <DOCKERHUB_USERNAME>/django_ec2