ARG GYM_IMAGE
FROM ${GYM_IMAGE}

# add env creator
COPY env_creator.py /opt/beobench/experiment_setup/
# add env creator to python path
ENV PYTHONPATH "${PYTHONPATH}:/opt/beobench/experiment_setup/"