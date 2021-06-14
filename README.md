# Accessing an ActiveMQ message broker using Skupper

Use public cloud resources to process data from a private message broker

* [Overview](#overview)
* [Prerequisites](#prerequisites)
* [Step 1: Configure separate console sessions](#step-1-configure-separate-console-sessions)
* [Step 2: Log in to your clusters](#step-2-log-in-to-your-clusters)
* [Step 3: Set the current namespaces](#step-3-set-the-current-namespaces)
* [Step 4: Install Skupper in your namespaces](#step-4-install-skupper-in-your-namespaces)
* [Step 5: Link your namespaces](#step-5-link-your-namespaces)
* [Step 6: Deploy the message broker](#step-6-deploy-the-message-broker)
* [Step 7: Expose the message broker](#step-7-expose-the-message-broker)
* [Step 8: Run the client](#step-8-run-the-client)

## Overview

This example is a simple message application that shows how you can
use Skupper to access an ActiveMQ broker at a remote site without
exposing it to the public internet.

It contains two services:

* An ActiveMQ broker named "broker1" running in a private data center.
  The broker has a queue named "queue1".

* An AMQP client running in the public cloud.  It sends 10 messages
  to "queue1" and then receives them back.

The example uses two Kubernetes namespaces, "private" and "public",
to represent the private data center and public cloud.

## Prerequisites

* The `kubectl` command-line tool, version 1.15 or later
  ([installation guide][install-kubectl])

* The `skupper` command-line tool, the latest version ([installation
  guide][install-skupper])

* Access to two Kubernetes namespaces, from any providers you choose,
  on any clusters you choose

[install-kubectl]: https://kubernetes.io/docs/tasks/tools/install-kubectl/
[install-skupper]: https://skupper.io/start/index.html#step-1-install-the-skupper-command-line-tool-in-your-environment


## Step 1: Configure separate console sessions

Skupper is designed for use with multiple namespaces, typically on
different clusters.  The `skupper` command uses your
[kubeconfig][kubeconfig] and current context to select the namespace
where it operates.

[kubeconfig]: https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/

Your kubeconfig is stored in a file in your home directory.  The
`skupper` and `kubectl` commands use the `KUBECONFIG` environment
variable to locate it.

A single kubeconfig supports only one active context per user.
Since you will be using multiple contexts at once in this
exercise, you need to create distinct kubeconfigs.

Start a console session for each of your namespaces.  Set the
`KUBECONFIG` environment variable to a different path in each
session.


Console for _public_:

~~~ shell
export KUBECONFIG=~/.kube/config-public
~~~

Console for _private_:

~~~ shell
export KUBECONFIG=~/.kube/config-private
~~~

## Step 2: Log in to your clusters

The methods for logging in vary by Kubernetes provider.  Find
the instructions for your chosen providers and use them to
authenticate and configure access for each console session.  See
the following links for more information:

* [Minikube](https://skupper.io/start/minikube.html#logging-in)
* [Amazon Elastic Kubernetes Service (EKS)](https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html)
* [Azure Kubernetes Service (AKS)](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough#connect-to-the-cluster)
* [Google Kubernetes Engine (GKE)](https://skupper.io/start/gke.html#logging-in)
* [IBM Kubernetes Service](https://skupper.io/start/ibmks.html#logging-in)
* [OpenShift](https://skupper.io/start/openshift.html#logging-in)


## Step 3: Set the current namespaces

Use `kubectl create namespace` to create the namespaces you wish to
use (or use existing namespaces).  Use `kubectl config set-context` to
set the current namespace for each session.


Console for _public_:

~~~ shell
kubectl create namespace public
kubectl config set-context --current --namespace public
~~~

Console for _private_:

~~~ shell
kubectl create namespace private
kubectl config set-context --current --namespace private
~~~

## Step 4: Install Skupper in your namespaces

The `skupper init` command installs the Skupper router and service
controller in the current namespace.  Run the `skupper init` command
in each namespace.

[minikube-tunnel]: https://skupper.io/start/minikube.html#running-minikube-tunnel

**Note:** If you are using Minikube, [you need to start `minikube
tunnel`][minikube-tunnel] before you install Skupper.


Console for _public_:

~~~ shell
skupper init
~~~

Console for _private_:

~~~ shell
skupper init --ingress none
~~~

## Step 5: Link your namespaces

Creating a link requires use of two `skupper` commands in conjunction,
`skupper token create` and `skupper link create`.

The `skupper token create` command generates a secret token that
signifies permission to create a link.  The token also carries the
link details.  The `skupper link create` command then uses the link
token to create a link to the namespace that generated it.

**Note:** The link token is truly a *secret*.  Anyone who has the
token can link to your namespace.  Make sure that only those you trust
have access to it.


Console for _public_:

~~~ shell
skupper token create ~/public.token
~~~

Console for _private_:

~~~ shell
skupper link create ~/public.token
skupper link status --wait 30
~~~

## Step 6: Deploy the message broker

Console for _private_:

~~~ shell
kubectl apply -f broker1.yaml
~~~

## Step 7: Expose the message broker

Console for _private_:

~~~ shell
skupper expose deployment/broker1 --port 5672
~~~

Console for _public_:

~~~ shell
kubectl get services
~~~

## Step 8: Run the client

Console for _public_:

~~~ shell
kubectl run client --attach --rm --restart Never --image quay.io/skupper/activemq-example-client --env SERVER=broker1
~~~