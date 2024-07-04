### Use this script by specifying the location of yamls in `deployment-script.sh`. Eg : 
##### KUBECONFIGS=("./kubeconfig_new.yaml" "./kubeconfig-personal.yaml") 

#### Usage : To run this script, use the command : `./deployment-script.sh`

##### Note : For simplicity, added a simple SASL over plaintext as a means of auth between kafka producers, consumers over port 9095. 

##### The deployment creates and exposes a load balancer over the kafka service. Use the external IP of the loadbalancer to access kafka. The same is printed as output for all the clusters.

#### Testing connectivity over cluster
##### The directory `test_scripts` has pykafka producer, consumer and admin clients with configured username, passwords for connecting to kafka brokers. 
##### The Kafka broker/cluster ip (i.e load balancer external ip) is defined and can be accessed and changed here.
##### In order to test the connectivity use the command : `python3 stats.py` -> This will return number of brokers and topics.
##### In order to send a test message, use : `python3 producer.py`
##### In order to consume a test message, use : `python3 consumer.py`