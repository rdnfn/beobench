# Example of using Celery-based containerized gym Environment

To run this example follow these steps:

1. Start containers: run `docker compose up` in this directory. This will launch two containers:
    - the environment container
    - the RabbitMQ message broker container (allowing for communication with the env container)
2. Run agent script: in another terminal use `python ./agent/agent.py` to run an example agent that uses the environment
3. Stop the containers by using `ctrl` + `c` in their process.

This example uses the `beobench.gym` API to define the communication between environment and agent.