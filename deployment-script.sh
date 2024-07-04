#!/bin/bash
KUBECONFIGS=("./kubeconfig_new.yaml" "./kubeconfig-personal.yaml")
# Deploy Kafka on each cluster and wait for external IP assignment
for kubeconfig in "${KUBECONFIGS[@]}"; do
  echo "deploying for $kubeconfig"
  ./deploy-kafka.sh $kubeconfig
done