AWS CodeBuild Test Postgres Database Example
==============================================================================
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Summary
------------------------------------------------------------------------------
In many projects, we need a database docker container for testing. We can easily run a container with an empty database, then destroy it automatically after testing. This repo gives you an example using AWS CodeBuild to run a "side-car" postgres container for testing.


The Example
------------------------------------------------------------------------------
In this example, we use the ``postgres:10.6-alpine`` image to run a postgres db in the background, and we use Python `sqlalchemy <https://www.sqlalchemy.org/>`_ to connect to the postgres db and run a `simple SQL statement <./tests/test_psql.py>`_.

The `buildspec.yml <./buildspec.yml>`_ file is the AWS CodeBuild orchestration file.

- In ``install`` phase, we pulled the docker image from DockerHub
- In ``pre_build`` phase, we start a background postgres container
- In ``build`` phase, we installed the dependencies and run the test
- In ``post_build`` phase, we destroy the postgres container.


DockerHub docker pull limits
------------------------------------------------------------------------------
The DockerHub has 100 pull per IP per hour limits. You may easily hit this limits if you have many build runs. I recommend to use AWS ECR to cache the image you pulled from DockerHub. There's NO COST to transfer data from ECR to AWS CodeBuild if they are in AWS Region, see explanation `here <https://aws.amazon.com/ecr/pricing/>`_. AWS ECR will charge if you are pulling from non AWS Region, for example, your local laptop.

In buildspec file, you should add some logic to ``install`` phase:

1. if ECR doesn't have this image, we pull it, then re-tag it, and then push to ECR.
2. if the latest image in ECR was updated one month before, we pull it form DockerHub and push it again to ECR.
3. in ``pre_build`` phase, we always use image from ECR.


Is this a "Side Car" or "Docker in Docker"?
------------------------------------------------------------------------------
You can think of AWS CodeBuild is a VM in sandbox mode. The main build logic happens in container, however you can setup additional background container. In other words, this is NOT "Docker in Docker".


References
------------------------------------------------------------------------------
- postgres on DockerHub: https://hub.docker.com/_/postgres
- Background tasks in build environments: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-background-tasks.html
