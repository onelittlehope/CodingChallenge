# Coding Challenge

For this project I've written a scalable and highly available service (MyNextBus) that will provide real-time data of buses and trains.


I chose not restrict the project to just the SF Muni agency since the api can handle any of the 63 agencies currently supported by the [NextBusXMLFeed](http://www.nextbus.com/xmlFeedDocs/NextBusXMLFeed.pdf) service. It didn't make sense to hard code the api to just the SF Muni agency.


The application is written in Python and uses Docker containers.


The Docker containers serve the stateless MyNextBus API and this service is made scalable + highly available because its containers are run under and managed by Kubernetes.


## Pre-requisites

* Ensure you have the following pre-requisites installed:
    * Docker >=1.12.5
    * kubectl >=1.5.1
    * minikube >=0.14.0
    * **Optional:** If you wish to develop against or run the Python service locally, you will also need:
        * Python >=2.7.12
        * [virtualenv](https://pypi.python.org/pypi/virtualenv)
        * [pip](https://pypi.python.org/pypi/pip/)


* To install Docker, follow the guide at: [https://docs.docker.com/engine/installation/](https://docs.docker.com/engine/installation/)


* To install kubectl, follow the guide at: [http://kubernetes.io/docs/user-guide/prereqs/](http://kubernetes.io/docs/user-guide/prereqs/)
    * The latest version can be downloaded and setup as easily as:
      ```
      # Linux
      curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl

      # OS X
      curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/darwin/amd64/kubectl
      ```


* To install minikube, follow the guide at: [http://kubernetes.io/docs/getting-started-guides/minikube/#installation](http://kubernetes.io/docs/getting-started-guides/minikube/#installation).
    * The latest version can be downloaded and setup as easily as:
      ```
      # Linux
      curl -Lo kubectl http://storage.googleapis.com/kubernetes-release/release/v1.5.1/bin/linux/amd64/kubectl && chmod +x kubectl && sudo mv kubectl /usr/local/bin/

      # OS X
      curl -Lo kubectl http://storage.googleapis.com/kubernetes-release/release/v1.5.1/bin/darwin/amd64/kubectl && chmod +x kubectl && sudo mv kubectl /usr/local/bin/
      ```

    * It is important to note that minikube requires:
        * Either VirtualBox (I've only tested with VirtualBox) or KVM installed
        * A CPU with VT-x/AMD-v virtualisation extensions
        * kubectl to be on the path


* **OPTIONAL:** If you wish to develop against or run the Python service locally, you can setup the virtualenv as follows:
    ```
    # Create virtualenv, activate it and install required Python modules
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt

    # Run the service
    python runserver.py

    # By default the service binds on 0.0.0.0 on TCP 8081. e.g.
    curl -H "accept:application/json" http://localhost:8081/agencies
    # or
    curl -H "accept:application/xml" http://localhost:8081/agencies
    ```


## Getting started

* Clone this git repository via:
    ```
    git clone git@github.com:onelittlehope/CodingChallenge.git
    ```


* Build / tag and push **your version** of the Docker container for this service to the Docker registry:
    ```
    # Build the Docker container
    docker build -t test1_img .

    # Tag the Docker container (replace docker_user_id with your docker user id)
    docker tag test1_img:latest docker_user_id/test1_img:0.1

    # Login to Docker registry
    docker login

    # Push the built image
    docker push docker_user_id/test1_img
    ```


* Run minikube and have it initialise a local Kubernetes cluster:
    ```
    minikube start

    # Example output:
    ---snip---
    Starting local Kubernetes cluster...
    Downloading Minikube ISO
    36.00 MB / 36.00 MB [==============================================] 100.00% 0s
    Kubectl is now configured to use the cluster.
    ---snip---
    ```


* Amend the MyNextBus replication controller definition file (mynextbus-rc.yml) and replace the existing image name with your Docker image name:
    ```
    # Change the line:
    image: jchoksi/test1_img:0.1

    # To:
    image: docker_user_id/test1_img:0.1
    ```


* Use kubectrl to create the MyNextBus replication controller and service:
    ```
    kubectl create -f mynextbus-rc.yml -f service.yml

    # Example output:
    ---snip---
    eplicationcontroller "mynextbus-rc" created
    service "mynextbus-service" created
    ---snip---
    ```


* Normally you can get information about the Kubernetes cluster via:
    ```
    kubectl cluster-info

    # E.g. output:
    ---snip---
    Kubernetes master is running at https://192.168.99.100:8443
    KubeDNS is running at https://192.168.99.100:8443/api/v1/proxy/namespaces/kube-system/services/kube-dns
    kubernetes-dashboard is running at https://192.168.99.100:8443/api/v1/proxy/namespaces/kube-system/services/kubernetes-dashboard

    To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
    ---snip---    
    ```
    However, the above url endpoints won't work properly with minikube due to the following bug: [https://github.com/kubernetes/dashboard/issues/692](https://github.com/kubernetes/dashboard/issues/692)

    If you try to access those end points you will get an *"Unauthorized"* page in Firefox and a *"This site can’t provide a secure connection. 192.168.99.100 doesn't adhere to security standards. ERR_SSL_SERVER_CERT_BAD_FORMAT"* page in Chrome.


* So to load the Kubernetes dashboard, enter:
    ```
    minikube service kubernetes-dashboard --namespace=kube-system
    ```
    Note: Running the above command will launch a browser with the Kubernetes dashboard page loaded.


* On the dashboard you should see the **mynextbus-rc** Replication Controller running 1 pod:

    ![01_replication_controller](https://cloud.githubusercontent.com/assets/3677874/21597470/145aa49a-d143-11e6-92d8-1d9667e82e4b.png)


* You can use the Actions menu to scale the replication controller to run more than one pod:

    ![02_scale_replication_controller](https://cloud.githubusercontent.com/assets/3677874/21597475/3fb08858-d143-11e6-9367-2829b29b839c.png)

    ![03_scale_replication_controller](https://cloud.githubusercontent.com/assets/3677874/21597496/90c81832-d143-11e6-88f7-3ab6d4b3fcdd.png)

    ![04_scale_replication_controller](https://cloud.githubusercontent.com/assets/3677874/21597501/9d583c6c-d143-11e6-8330-83486090939c.png)


* To access the LoadBalanced MyNextBus service, you need to run the following command:
    ```
    minikube service mynextbus-service
    ```

    Note: Running the above command will launch a browser with the MyNextBus service page loaded.

    This is needed because minicube doesn't have the ability to setup an external load balancer (yet) according to the following issue: [https://github.com/kubernetes/minikube/issues/384](https://github.com/kubernetes/minikube/issues/384)

    ![05_mynextbus_service](https://cloud.githubusercontent.com/assets/3677874/21597512/c79dff7a-d143-11e6-9094-325b94a1f96b.png)

    ![06_mynextbus_service](https://cloud.githubusercontent.com/assets/3677874/21597514/d2aaf4d6-d143-11e6-9d9a-c800c6d03cb9.png)


* You can confirm that Kubernetes is load balancing requests across the different pods by looking at each pods logs after making several requests to the MyNextBus service.

    ![07_kubernetes_pod_logs](https://cloud.githubusercontent.com/assets/3677874/21597524/f845f484-d143-11e6-939f-905c604c53e0.png)

    ![08_kubernetes_pod_logs](https://cloud.githubusercontent.com/assets/3677874/21597529/032092ba-d144-11e6-9933-e8fec901878d.png)    


## Notes

The above is a proof of concept of how Kubernetes could be used to setup a scalable and highly available web service.


* Requirement 1 of the coding challenge was met as the MyNextBus service does expose all of the endpoints in the NextBus API.


* Requirement 2 of the coding challenge was met by the ```/inactiveroutes/<string:agency_tag>/<int:epoch_time>``` endpoint.


* Requirement 3 of the coding challenge was met by the ```/totalqueries``` + ```/slowqueries``` endpoints. Note, due to the requirement that the web service remain stateless, I chose not to store the query stats outside the web service and hence if you want an accurate count/view of the total queries / slow queries, you would need to run the two end points on each pod and tally up the output generated. The alternative would have been to store the stats in a redis cache.


* Requirement 4 of the coding challenge was met because you can control the output returned by the MyNextBus service via the HTTP Accept header. e.g.

    ```
    # Replace localhost:8081 with the LoadBalanced url/port:

    curl -H "accept:application/json" http://localhost:8081/agencies
    curl -H "accept:application/x-xml" http://localhost:8081/agencies
    curl -H "accept:application/xml" http://localhost:8081/agencies
    curl -H "accept:misc/both" http://localhost:8081/agencies
    curl -H "accept:text/xml" http://localhost:8081/agencies

    ```


* Requirement 5 of coding challenge requires that the NextBusXMLFeed service be accessed via a caching HTTP proxy which will stop the NextBusXMLFeed service from being hurt as the same requests won't be made more than the configured caching interval period. This requirement has not been met as I've run out of time to document setting up a Varnish caching http proxy. I've put in code in the config.py which allows you to setup a http or https proxy and this can also be controlled via the HTTP_PROXY + HTTPS_PROXY environment variables but I've not setup a caching proxy to test that this requirement is met.


Lastly, I've not implemented any unit tests for the api due to time constraints.
