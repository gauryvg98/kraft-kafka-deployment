#!/bin/bash

# Check if kubeconfig is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <kubeconfig>"
  exit 1
fi

KUBECONFIG=$1

export KUBECONFIG=$KUBECONFIG
kubectl create ns kafka || true

# Apply the StatefulSet
kubectl apply -f kafka-statefulset.yaml -n kafka

# Apply the Service
kubectl apply -f kafka-service.yaml -n kafka

# Wait for the LoadBalancer IP to be assigned
echo "Waiting for LoadBalancer IP..."
while true; do
  EXTERNAL_IP=$(kubectl get svc kafka -n kafka -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
  if [ ! -z "$EXTERNAL_IP" ]; then
    break
  fi
  echo "Waiting for external IP..."
  sleep 10
done

# Print the external IP for verification
echo "External IP: $EXTERNAL_IP"

# Update the ConfigMap with the actual external IP and save it to a temporary file
sed "s/YOUR_EXTERNAL_IP/$EXTERNAL_IP/g" kafka-configmap.yaml > /tmp/kafka-configmap.yaml

# Apply the updated ConfigMap
kubectl apply -f /tmp/kafka-configmap.yaml -n kafka

# Wait for the Kafka Pod to be running
echo "Waiting for Kafka Pod to be running..."
kubectl wait --for=condition=ready pod -l app=kafka --timeout=300s -n kafka

echo "Kafka deployment completed. Kafka should be accessible from outside the cluster."
