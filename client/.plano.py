#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from plano import *

image_tag = "quay.io/skupper/activemq-example-client"

@command
def build(no_cache=False):
    run("mvn package")

    no_cache_arg = "--no-cache" if no_cache else ""

    run(f"podman build {no_cache_arg} --format docker -t {image_tag} .")

@command
def clean():
    run("mvn clean")

@command
def run_():
    run(f"podman run --net host {image_tag} --host localhost --port 8080 --backend http://localhost:8081")

# @command(name="run")
# def run_():
#     run("java -jar target/quarkus-app/quarkus-run.jar")

# @command
# def run_broker():
#     run("podman run -it -p 5672:5672 -e AMQ_USER=example -e AMQ_PASSWORD=example quay.io/artemiscloud/activemq-artemis-broker")

@command
def debug():
    run(f"podman run -it --net host --entrypoint /bin/sh {image_tag}")

@command
def push():
    run("podman login quay.io")
    run(f"podman push {image_tag}")

# @command
# def build_image():
#     build()
#     run("podman build -t quay.io/skupper/activemq-example-client .")

# @command
# def push_image():
#     build_image()
#     run("podman push quay.io/skupper/activemq-example-client")
