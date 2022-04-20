ARG PREV_IMAGE
# package type is either local or pypi
ARG PACKAGE_TYPE="pypi"

# conditional build (see https://stackoverflow.com/a/54245466)
FROM ${PREV_IMAGE} as pypi_beobench
ARG PACKAGE="beobench"
ONBUILD ENV INSTALL_PACKAGE ${PACKAGE}

FROM ${PREV_IMAGE} as local_beobench
ARG PACKAGE="beobench"
ONBUILD COPY . /tmp/beobench_repo/
ONBUILD ENV INSTALL_PACKAGE /tmp/beobench_repo

FROM ${PACKAGE_TYPE}_beobench
# install beobench
ARG EXTRAS="extended,rllib"
RUN pip --disable-pip-version-check --no-cache-dir install "${INSTALL_PACKAGE}[${EXTRAS}]"