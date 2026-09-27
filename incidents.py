"""
Simulated Kubernetes Incidents Data for Anmol AI Ops Incident Investigator.
This file provides structured, realistic operational signals (Pod status, events, logs)
for AKS / Kubernetes troubleshooting scenarios.
"""

INCIDENTS = {
    "CrashLoopBackOff": {
        "id": "crashloopbackoff",
        "title": "CrashLoopBackOff - Missing Environment Variable",
        "category": "CrashLoopBackOff",
        "pod_name": "payment-api-7f8d9",
        "namespace": "production",
        "status": "CrashLoopBackOff",
        "node": "aks-nodepool1-38291047-vmss000002",
        "restart_count": 14,
        "exit_code": 1,
        "description": "Payment API microservice failing on startup due to unhandled configuration error.",
        "status_brief": "The container continuously starts, crashes, and attempts to restart. Kubernetes applies an exponential back-off delay (10s up to 5m) between restart attempts to prevent node resource exhaustion.",
        "pod_details": """Name:         payment-api-7f8d9
Namespace:    production
Node:         aks-nodepool1-38291047-vmss000002/10.240.0.5
Start Time:   Sun, 27 Sep 2026 11:45:10 +0000
Labels:       app=payment-api
              pod-template-hash=7f8d9
Status:       Running
IP:           10.244.1.42
Containers:
  payment-container:
    Container ID:   containerd://e4b9f8d1c2a3...
    Image:          myregistry.azurecr.io/payment-api:v2.4.1
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       Error
      Exit Code:    1
      Started:      Sun, 27 Sep 2026 12:02:11 +0000
      Finished:     Sun, 27 Sep 2026 12:02:13 +0000
    Ready:          False
    Restart Count:  14
    Limits:
      cpu:     500m
      memory:  512Mi
    Requests:
      cpu:     100m
      memory:  256Mi""",
        "events": [
            {"time": "0m", "type": "Warning", "reason": "BackOff", "object": "pod/payment-api-7f8d9", "message": "Back-off restarting failed container payment-container in pod payment-api-7f8d9_production"},
            {"time": "1m", "type": "Normal", "reason": "Pulled", "object": "pod/payment-api-7f8d9", "message": "Container image \"myregistry.azurecr.io/payment-api:v2.4.1\" already present on machine"},
            {"time": "1m", "type": "Normal", "reason": "Created", "object": "pod/payment-api-7f8d9", "message": "Created container payment-container"},
            {"time": "1m", "type": "Normal", "reason": "Started", "object": "pod/payment-api-7f8d9", "message": "Started container payment-container"},
            {"time": "2m", "type": "Warning", "reason": "Unhealthy", "object": "pod/payment-api-7f8d9", "message": "Liveness probe failed: HTTP probe failed with statuscode 500"}
        ],
        "logs": """[2026-09-27 12:02:11] [INFO] Starting payment-api microservice v2.4.1...
[2026-09-27 12:02:11] [INFO] Initializing runtime context & loading configuration...
[2026-09-27 12:02:12] [INFO] Connecting to PostgreSQL database cluster...
[2026-09-27 12:02:12] [ERROR] DATABASE_URL environment variable not found
[2026-09-27 12:02:12] [CRITICAL] Application startup failed. Fatal exception encountered during DB initialization module.
[2026-09-27 12:02:12] [INFO] Process exiting with status code 1."""
    },

    "OOMKilled": {
        "id": "oomkilled",
        "title": "OOMKilled - Container Exceeded Memory Limit",
        "category": "OOMKilled",
        "pod_name": "analytics-worker-5c4db468-x9z2l",
        "namespace": "analytics",
        "status": "OOMKilled",
        "node": "aks-nodepool1-38291047-vmss000003",
        "restart_count": 5,
        "exit_code": 137,
        "description": "Analytics data stream processing pod terminated by Linux kernel OOM Killer after memory limit breach.",
        "status_brief": "The Linux kernel Out-Of-Memory (OOM) Killer abruptly terminated the container (Exit Code 137) because its memory consumption exceeded the strict RAM limit defined in the Pod spec.",
        "pod_details": """Name:         analytics-worker-5c4db468-x9z2l
Namespace:    analytics
Node:         aks-nodepool1-38291047-vmss000003/10.240.0.6
Start Time:   Sun, 27 Sep 2026 11:30:00 +0000
Labels:       app=analytics-worker
Status:       Running
IP:           10.244.2.19
Containers:
  worker:
    Container ID:   containerd://a1b2c3d4e5f6...
    Image:          myregistry.azurecr.io/analytics-worker:v1.8.0
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       OOMKilled
      Exit Code:    137
      Started:      Sun, 27 Sep 2026 12:01:00 +0000
      Finished:     Sun, 27 Sep 2026 12:04:45 +0000
    Ready:          False
    Restart Count:  5
    Limits:
      cpu:     1000m
      memory:  512Mi
    Requests:
      cpu:     250m
      memory:  256Mi""",
        "events": [
            {"time": "1m", "type": "Warning", "reason": "OOMKilling", "object": "pod/analytics-worker-5c4db468-x9z2l", "message": "Memory cgroup out of memory: Killed process 14829 (python3) total-vm:1849200kB, anon-rss:524188kB"},
            {"time": "1m", "type": "Warning", "reason": "BackOff", "object": "pod/analytics-worker-5c4db468-x9z2l", "message": "Back-off restarting failed container worker in pod analytics-worker-5c4db468-x9z2l_analytics"},
            {"time": "3m", "type": "Normal", "reason": "Started", "object": "pod/analytics-worker-5c4db468-x9z2l", "message": "Started container worker"}
        ],
        "logs": """[2026-09-27 12:01:02] [INFO] Analytics Worker started. Fetching batch tasks from queue...
[2026-09-27 12:02:15] [INFO] Processing batch dataset batch_id=98412 (Size: 450 MB uncompressed)
[2026-09-27 12:03:30] [WARNING] High memory consumption detected: 412Mi / 512Mi (80.4%)
[2026-09-27 12:04:10] [WARNING] Memory usage near container limit: 508Mi / 512Mi (99.2%)
[2026-09-27 12:04:45] [FATAL] Signal 9 (SIGKILL) received from kernel (OOMKilled). Process terminated abruptly."""
    },

    "ImagePullBackOff": {
        "id": "imagepullbackoff",
        "title": "ImagePullBackOff - ACR Authentication Failure",
        "category": "ImagePullBackOff",
        "pod_name": "order-processor-689b9d-4k8mn",
        "namespace": "ecommerce",
        "status": "ImagePullBackOff",
        "node": "aks-nodepool1-38291047-vmss000001",
        "restart_count": 0,
        "exit_code": None,
        "description": "Deployment cannot start because kubelet failed to pull container image from Azure Container Registry (ACR).",
        "status_brief": "Kubelet cannot pull the requested container image from the registry (e.g., Azure Container Registry). Common causes include missing registry credentials, missing ACR role assignments, or non-existent image tags.",
        "pod_details": """Name:         order-processor-689b9d-4k8mn
Namespace:    ecommerce
Node:         aks-nodepool1-38291047-vmss000001/10.240.0.4
Start Time:   Sun, 27 Sep 2026 12:00:00 +0000
Labels:       app=order-processor
Status:       Pending
IP:           10.244.0.88
Containers:
  processor:
    Container ID:   
    Image:          prodacr3849.azurecr.io/ecommerce/order-processor:v3.1.0
    State:          Waiting
      Reason:       ImagePullBackOff
    Ready:          False
    Restart Count:  0
    Limits:
      cpu:     200m
      memory:  256Mi
    Requests:
      cpu:     100m
      memory:  128Mi""",
        "events": [
            {"time": "3m", "type": "Normal", "reason": "Scheduled", "object": "pod/order-processor-689b9d-4k8mn", "message": "Successfully assigned ecommerce/order-processor-689b9d-4k8mn to aks-nodepool1-38291047-vmss000001"},
            {"time": "2m", "type": "Normal", "reason": "Pulling", "object": "pod/order-processor-689b9d-4k8mn", "message": "Pulling image \"prodacr3849.azurecr.io/ecommerce/order-processor:v3.1.0\""},
            {"time": "2m", "type": "Warning", "reason": "Failed", "object": "pod/order-processor-689b9d-4k8mn", "message": "Failed to pull image \"prodacr3849.azurecr.io/ecommerce/order-processor:v3.1.0\": rpc error: code = Unknown desc = failed to pull and unpack image \"prodacr3849.azurecr.io/ecommerce/order-processor:v3.1.0\": failed to resolve reference \"prodacr3849.azurecr.io/ecommerce/order-processor:v3.1.0\": unexpected status from HEAD request to https://prodacr3849.azurecr.io/v2/ecommerce/order-processor/manifests/v3.1.0: 401 Unauthorized - unauthorized: authentication required"},
            {"time": "1m", "type": "Warning", "reason": "Failed", "object": "pod/order-processor-689b9d-4k8mn", "message": "Error: ErrImagePull"},
            {"time": "0m", "type": "Warning", "reason": "BackOff", "object": "pod/order-processor-689b9d-4k8mn", "message": "Back-off pulling image \"prodacr3849.azurecr.io/ecommerce/order-processor:v3.1.0\""}
        ],
        "logs": """[KUBELET TELEMETRY LOGS]
Unable to fetch container stdout logs because container was never created.
Error: Container 'processor' in pod 'order-processor-689b9d-4k8mn' has not started due to ImagePullBackOff.

Kubelet Image Pull Audit Log:
- Target Registry: prodacr3849.azurecr.io
- Target Repository: ecommerce/order-processor:v3.1.0
- Auth Mechanism: Managed Identity / ACR Pull Role Assignment
- HTTP Status: 401 Unauthorized
- Error Detail: unauthorized: authentication required. Image pull secret or Azure Role Assignment (AcrPull) missing or expired."""
    },

    "Readiness Probe Failure": {
        "id": "readiness_probe_failure",
        "title": "Readiness Probe Failure - 503 Service Unavailable",
        "category": "Readiness Probe Failure",
        "pod_name": "frontend-gateway-79d865b4c-jp28s",
        "namespace": "web",
        "status": "Readiness Probe Failed (0/1 Ready)",
        "node": "aks-nodepool1-38291047-vmss000002",
        "restart_count": 0,
        "exit_code": 0,
        "description": "Frontend pod container is running but remains unready (0/1), causing Kubernetes Service endpoints to exclude traffic.",
        "status_brief": "The container process is running, but its readiness check (e.g. GET /readyz) failed. Kubernetes temporarily removes the Pod IP from Service Endpoint routing so no live traffic reaches the unready container.",
        "pod_details": """Name:         frontend-gateway-79d865b4c-jp28s
Namespace:    web
Node:         aks-nodepool1-38291047-vmss000002/10.240.0.5
Start Time:   Sun, 27 Sep 2026 11:50:00 +0000
Labels:       app=frontend-gateway
Status:       Running
IP:           10.244.1.99
Containers:
  gateway:
    Container ID:   containerd://c7d8e9f0a1b2...
    Image:          myregistry.azurecr.io/frontend-gateway:v1.2.0
    State:          Running
      Started:      Sun, 27 Sep 2026 11:50:02 +0000
    Ready:          False
    Restart Count:  0
    Readiness:      http-get http://:8080/readyz delay=5s timeout=2s period=10s #success=1 #failure=3
    Limits:
      cpu:     500m
      memory:  512Mi
    Requests:
      cpu:     100m
      memory:  256Mi""",
        "events": [
            {"time": "5m", "type": "Normal", "reason": "Started", "object": "pod/frontend-gateway-79d865b4c-jp28s", "message": "Started container gateway"},
            {"time": "3m", "type": "Warning", "reason": "Unhealthy", "object": "pod/frontend-gateway-79d865b4c-jp28s", "message": "Readiness probe failed: HTTP probe failed with statuscode: 503"},
            {"time": "1m", "type": "Warning", "reason": "Unhealthy", "object": "pod/frontend-gateway-79d865b4c-jp28s", "message": "Readiness probe failed: HTTP probe failed with statuscode: 503"}
        ],
        "logs": """[2026-09-27 11:50:02] [INFO] Nginx/Node.js Gateway initialized. Listening on port 8080.
[2026-09-27 11:50:05] [INFO] Executing readiness check sequence...
[2026-09-27 11:50:05] [INFO] Checking dependency: Auth Microservice (auth-svc.production.svc.cluster.local:4000) ... OK
[2026-09-27 11:50:06] [ERROR] Checking dependency: Redis Cache (redis-cluster.cache.svc.cluster.local:6379) ... FAILED (Connection Refused)
[2026-09-27 11:50:15] [WARNING] Readiness probe endpoint GET /readyz returned HTTP 503: Subsystem 'redis-cache' not initialized.
[2026-09-27 11:50:25] [WARNING] Readiness probe endpoint GET /readyz returned HTTP 503: Subsystem 'redis-cache' not initialized."""
    },

    "PVC Pending": {
        "id": "pvc_pending",
        "title": "PVC Pending - Unbound PersistentVolumeClaim",
        "category": "PVC Pending",
        "pod_name": "data-indexer-0",
        "namespace": "storage",
        "status": "Pending",
        "node": "Unassigned",
        "restart_count": 0,
        "exit_code": None,
        "description": "StatefulSet pod data-indexer-0 cannot be scheduled because its PersistentVolumeClaim (pvc-data-indexer-0) is unbound.",
        "status_brief": "The Pod cannot be scheduled or initialized because its PersistentVolumeClaim (PVC) is unbound, waiting for dynamic storage provisioner allocation, or constrained by availability zone storage limits.",
        "pod_details": """Name:         data-indexer-0
Namespace:    storage
Node:         <none>
Labels:       app=data-indexer
              controller-revision-hash=data-indexer-784d856
              statefulset.kubernetes.io/pod-name=data-indexer-0
Status:       Pending
IP:           
Containers:
  indexer:
    Image:      myregistry.azurecr.io/data-indexer:v4.0.0
    State:      Waiting
      Reason:   ContainerCreating
    Ready:      False
    Volume Mounts:
      /var/data from data-volume (rw)
Volumes:
  data-volume:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  pvc-data-indexer-0
    ReadOnly:   false""",
        "events": [
            {"time": "8m", "type": "Warning", "reason": "FailedScheduling", "object": "pod/data-indexer-0", "message": "0/3 nodes are available: 3 pod has unbound immediate PersistentVolumeClaims. preemption: 0/3 nodes are available: 3 Preemption is not helpful for scheduling."},
            {"time": "5m", "type": "Warning", "reason": "FailedScheduling", "object": "pod/data-indexer-0", "message": "0/3 nodes are available: 3 pod has unbound immediate PersistentVolumeClaims."},
            {"time": "2m", "type": "Normal", "reason": "ExternalProvisioning", "object": "persistentvolumeclaim/pvc-data-indexer-0", "message": "Waiting for a volume to be created by external-provisioner \"disk.csi.azure.com\" or volume requested is not available in zone az-1"}
        ],
        "logs": """[KUBE-SCHEDULER & CSI DRIVER LOGS]
Pod data-indexer-0 is in Pending state.
Container execution has not started because persistent storage volume attachment is incomplete.

PVC Status Audit:
- Claim Name: pvc-data-indexer-0
- Requested Storage: 100Gi (managed-csi-premium)
- VolumeBindingMode: Immediate
- Provisioner: disk.csi.azure.com (Azure Disk CSI Driver)
- Error: Volume provisioning stalled. StorageClass 'managed-csi-premium' quota exceeded or requested disk size unavailable in target Availability Zone."""
    }
}
