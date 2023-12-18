#!/bin/bash
# shellcheck disable=SC2153

function yellow() { printf "\x1b[38;5;227m%s\e[0m " "${@}"; printf "\n"; }
function warn() { printf "\x1b[38;5;208m%s\e[0m " "${@}"; printf "\n"; }
function green() { printf "\x1b[38;5;048m%s\e[0m " "${@}"; printf "\n"; }
function red() { printf "\x1b[38;5;196m%s\e[0m " "${@}"; printf "\n"; }

function build_container_image() {
    push_enabled="0"
    image_file="./derived.Dockerfile"
    container_reg_username="matlokai"
    image_name="blender-ai-demos"
    container_reg_name="docker.io"
    push_image_name="${container_reg_name}/${container_reg_username}/${image_name}"

    yellow "building ${push_image_name} image with ${image_file}"
    vc="time podman build -f ${image_file} --no-cache --rm -t ${push_image_name} ."
    echo "${vc}"
    eval "${vc}"
    lt="$?"
    if [[ "${lt}" -ne 0 ]]; then
        red "error - failed to build ${push_image_name} container image - stopping"
        echo -e "\n${vc}\n"
        exit 1
    fi
    echo "build done - getting image id"
    vc="podman images | grep \"${push_image_name}\" | head -1 | awk '{print \$3}'"
    echo "${vc}"
    latest_image=$(eval "${vc}")
    lt="$?"
    if [[ "${lt}" -ne 0 ]]; then
        red "error - failed to find ${push_image_name} container image - stopping"
        echo -e "\n${vc}\n"
        exit 1
    fi
    if [[ "${latest_image}" == "" ]]; then
        red "error - failed to find a non-empty image with name: ${push_image_name} - stopping"
        echo -e "\n${vc}\n"
        exit 1
    fi
    # disable push if not enabled/not set
    if [[ "${push_enabled}" -eq 1 ]]; then
        echo "image ${latest_image} for push: ${push_image_name}"
        vc="podman tag ${latest_image} ${push_image_name}"
        echo "${vc}"
        eval "${vc}"
        lt="$?"
        if [[ "${lt}" -ne 0 ]]; then
            red "error - failed to tag ${push_image_name} container image - stopping"
            echo -e "\n${vc}\n"
            exit 1
        fi
        yellow "pushing: ${push_image_name}"
        vc="podman push ${push_image_name}"
        echo "${vc}"
        eval "${vc}"
        lt="$?"
        if [[ "${lt}" -ne 0 ]]; then
            red "error - failed to push ${image_name} container image to: ${push_image_name} - stopping"
            echo -e "\n${vc}\n"
            exit 1
        fi
    else
        echo "not pushing image: ${latest_image} push=${push_enabled}"
    fi
    green "done building container image: ${push_image_name}:latest"
}

build_container_image

exit 0
