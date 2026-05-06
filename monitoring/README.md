# Monitoring
Prometheus installed via Helm on both EKS and AKS.
Namespace: monitoring
Query used: kube_pod_status_phase{namespace="default",phase="Running"}
Result: 3 Running pods confirmed on both clusters.
