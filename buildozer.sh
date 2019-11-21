#!/usr/bin/env bash

# https://hub.docker.com/r/kivy/buildozer/dockerfile

BUILDOZER_USER_DIR=/mnt/data/app/soft/coding/buildozer_user
BUILDOZER_DIR="${BUILDOZER_USER_DIR}/.buildozer"

create_temp_container() {
    docker run --interactive --tty --rm \
        --volume ${BUILDOZER_USER_DIR}:/home/user \
        --volume "${PWD}":/home/user/hostcwd \
        --volume "${BUILDOZER_DIR}":/home/user/hostcwd/.buildozer \
        --entrypoint /bin/bash kivy/buildozer
}

create_container() {
    docker run --name buildozer -h buildozer --interactive --tty \
        --volume ${BUILDOZER_USER_DIR}:/home/user \
        --volume "${PWD}":/home/user/hostcwd \
        --volume "${BUILDOZER_DIR}":/home/user/hostcwd/.buildozer \
        --entrypoint /bin/bash kivy/buildozer
}

start_container() {
    docker start buildozer -i
}

create_temp_container
