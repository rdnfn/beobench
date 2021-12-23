def start_experiment_container() -> None:

    # build container
    # docker build -t beobench:latest -f ./docker/Dockerfile.experiments .

    # create docker network
    # docker network create beobench-net

    # run docker container
    # docker run -v /var/run/docker.sock:/var/run/docker.sock --network=beobench-net --name exp1 beobench /bin/bash -c "python -m pip install git+https://github.com/rdnfn/beobench && export WANDB_API_KEY=XYZZZZZZZZZZZZZ && python -m beobench.scheduler --use-wandb && bash"

    pass
