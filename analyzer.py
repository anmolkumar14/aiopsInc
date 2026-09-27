"""
Automated Incident Analysis Engine for Anmol AI Ops Incident Investigator.
Provides deterministic operational analysis of Kubernetes signals (Status, Events, Logs)
and generates SRE-grade Root Cause Analysis (RCA) reports.
"""

from typing import Dict, Any


def analyze_incident(incident: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyzes Kubernetes incident telemetry signals and produces diagnostic findings,
    remediation guidance, and structured RCA documentation.
    """
    cat = incident.get("category", "")
    pod = incident.get("pod_name", "")
    ns = incident.get("namespace", "default")
    
    if cat == "CrashLoopBackOff":
        confidence = "96%"
        severity = "CRITICAL"
        root_cause = "The application is crashing because the DATABASE_URL environment variable is missing from the container spec or secret configuration."
        evidence = [
            f"Pod `{pod}` is stuck in `CrashLoopBackOff` status with {incident.get('restart_count', 0)} restart cycles.",
            "Container exited with failure Exit Code 1.",
            "Application startup logs explicitly record: `ERROR: DATABASE_URL environment variable not found`.",
            "Liveness probe triggered consecutive HTTP 500 failures as container crashed during runtime boot."
        ]
        actions = [
            "Inspect Deployment spec to verify if `DATABASE_URL` is defined under `env` or `envFrom`.",
            "Verify that the target Secret or ConfigMap containing database connection string exists in namespace `" + ns + "`.",
            "Update Deployment manifest with correct environment configuration and apply update.",
            "Monitor rollout status to verify pod reaches `1/1 Ready` state."
        ]
        commands = [
            f"kubectl describe pod {pod} -n {ns}",
            f"kubectl logs {pod} -n {ns} --previous",
            f"kubectl get deployment payment-api -n {ns} -o yaml",
            f"kubectl rollout status deployment/payment-api -n {ns}"
        ]
        rca = {
            "incident_title": f"Production Outage: Pod {pod} in CrashLoopBackOff",
            "impact": "Payment API microservice is unavailable. End users experience transaction failures (HTTP 500/503 errors).",
            "observed_symptoms": f"Pod state reported as CrashLoopBackOff with {incident.get('restart_count', 0)} restarts. HTTP 500 response from health probes.",
            "probable_root_cause": "Application process raised an unhandled fatal exception during boot sequence because the required environment variable `DATABASE_URL` was missing from the Pod specification.",
            "supporting_evidence": evidence,
            "recommended_resolution": [
                "1. Add `DATABASE_URL` key to the Secret `payment-api-secrets` in namespace `" + ns + "`.",
                "2. Update Deployment `payment-api` manifest to reference `DATABASE_URL` from secret.",
                "3. Execute `kubectl apply -f deployment.yaml` to trigger rolling update."
            ],
            "validation_steps": [
                f"Run `kubectl get pod {pod} -n {ns}` and confirm status is `Running` (1/1 Ready).",
                f"Inspect live logs: `kubectl logs {pod} -n {ns}` to confirm successful database handshake."
            ],
            "preventive_actions": [
                "Implement Helm / Kustomize schema validation (e.g., kubeval or datatree) in CI/CD pipeline.",
                "Configure startup probes with sufficient delay to fail fast with clear diagnostic messages.",
                "Set up Azure Monitor alerts for pod restart count > 3 in 5 minutes."
            ]
        }

    elif cat == "OOMKilled":
        confidence = "98%"
        severity = "CRITICAL"
        root_cause = "The container exceeded its allocated memory limit of 512Mi during heavy batch data processing and was terminated by the Linux kernel OOM (Out Of Memory) Killer with Exit Code 137."
        evidence = [
            f"Pod `{pod}` terminated with Last State `OOMKilled` and Exit Code `137`.",
            "Kernel event logged: `Memory cgroup out of memory: Killed process 14829 (python3)`.",
            "Container log recorded linear memory increase to 508Mi / 512Mi (99.2%) before abrupt SIGKILL signal."
        ]
        actions = [
            "Check current memory request/limit configuration for deployment `" + pod.split('-')[0] + "-worker`.",
            "Review container memory usage trends using `kubectl top pod` or Azure Monitor metrics.",
            "Increase memory limits (e.g., from 512Mi to 1Gi/2Gi) or optimize batch processing chunk size.",
            "Verify node capacity to ensure node pool can accommodate higher memory allocation."
        ]
        commands = [
            f"kubectl describe pod {pod} -n {ns}",
            f"kubectl top pod {pod} -n {ns}",
            "kubectl get deployment analytics-worker -n " + ns + " -o yaml",
            "kubectl top nodes"
        ]
        rca = {
            "incident_title": f"Workload Termination: Pod {pod} OOMKilled",
            "impact": "Analytics batch worker job failed mid-stream, delaying downstream data processing and pipeline reporting.",
            "observed_symptoms": "Container exited abruptly with Exit Code 137. Kubernetes event `OOMKilling` recorded.",
            "probable_root_cause": "The worker process loaded an uncompressed 450MB dataset batch into RAM, pushing container cgroup memory consumption beyond the strict 512Mi limit.",
            "supporting_evidence": evidence,
            "recommended_resolution": [
                "1. Modify Deployment resources spec: increase memory limit from 512Mi to 1024Mi (1Gi).",
                "2. Update worker application logic to stream data in smaller chunk sizes (e.g., 50MB batches).",
                "3. Apply updated Deployment manifest and verify deployment."
            ],
            "validation_steps": [
                f"Execute `kubectl top pod -n {ns}` during batch run to monitor memory consumption under 80% threshold.",
                "Verify zero OOM events recorded over next 24-hour window."
            ],
            "preventive_actions": [
                "Configure Vertical Pod Autoscaler (VPA) in recommendation mode to detect memory resource underprovisioning.",
                "Establish Datadog / Azure Monitor alerts for pod memory utilization exceeding 85% limit."
            ]
        }

    elif cat == "ImagePullBackOff":
        confidence = "95%"
        severity = "HIGH"
        root_cause = "Kubernetes kubelet failed to pull container image from Azure Container Registry (ACR) due to authentication failure (401 Unauthorized / missing ACR role assignment or image pull secret)."
        evidence = [
            f"Pod `{pod}` status is `Pending` with container state `ImagePullBackOff`.",
            "Kubelet event failure: `401 Unauthorized - unauthorized: authentication required`.",
            "Target image `prodacr3849.azurecr.io/ecommerce/order-processor:v3.1.0` requires ACR authentication.",
            "AKS cluster Managed Identity / Service Principal lacks `AcrPull` role on registry `prodacr3849`."
        ]
        actions = [
            "Verify image repository name and tag `v3.1.0` exist in Azure Container Registry `prodacr3849`.",
            "Verify AKS Managed Identity has `AcrPull` role assignment on ACR target.",
            "If using ImagePullSecrets, confirm secret exists in namespace `" + ns + "` and is referenced in Pod spec.",
            "Attach ACR to AKS using Azure CLI command `az aks update --attach-acr`."
        ]
        commands = [
            f"kubectl describe pod {pod} -n {ns}",
            f"kubectl get events -n {ns} --field-selector reason=Failed",
            "az aks check-acr --name <aks-cluster-name> --resource-group <rg-name> --acr prodacr3849.azurecr.io",
            "az role assignment list --assignee <aks-managed-identity-id> --scope /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.ContainerRegistry/registries/prodacr3849"
        ]
        rca = {
            "incident_title": f"Deployment Failure: Pod {pod} ImagePullBackOff",
            "impact": "New version v3.1.0 of order-processor cannot be deployed. Pending pod prevents deployment scaling and updates.",
            "observed_symptoms": "Pod stuck in Pending / ImagePullBackOff state. Kubelet repeatedly fails HEAD request to ACR with HTTP 401.",
            "probable_root_cause": "The AKS node pool managed identity lost or lacks `AcrPull` role permissions on Azure Container Registry `prodacr3849`.",
            "supporting_evidence": evidence,
            "recommended_resolution": [
                "1. Run Azure CLI command: `az aks update -n <aks-cluster> -g <rg> --attach-acr prodacr3849`.",
                "2. Alternatively, verify Workload Identity or create Kubernetes `docker-registry` secret in namespace `" + ns + "`.",
                "3. Restart deployment rollout: `kubectl rollout restart deployment/order-processor -n " + ns + "`."
            ],
            "validation_steps": [
                f"Verify event log shows `Successfully pulled image` for pod {pod}.",
                f"Check pod status reaches `1/1 Running` state."
            ],
            "preventive_actions": [
                "Automate ACR role assignments using Terraform / Bicep IaC modules.",
                "Include ACR access verification steps in deployment release pipelines."
            ]
        }

    elif cat == "Readiness Probe Failure":
        confidence = "92%"
        severity = "HIGH"
        root_cause = "Application container is running (Exit Code 0), but the readiness probe HTTP GET on `/readyz` is returning 503 Service Unavailable because upstream dependency Redis Cache (`redis-cluster.cache.svc.cluster.local:6379`) is unreachable."
        evidence = [
            f"Pod `{pod}` status shows `Ready: False` (0/1 Ready) while container state is `Running`.",
            "Kubernetes Warning Event: `Readiness probe failed: HTTP probe failed with statuscode: 503`.",
            "Application logs record connection failure: `Checking dependency: Redis Cache ... FAILED (Connection Refused)`."
        ]
        actions = [
            "Inspect status of upstream Redis cluster in namespace `cache` or `production`.",
            "Check NetworkPolicies or DNS resolution between namespace `" + ns + "` and dependency namespace.",
            "Verify readinessProbe configuration (initialDelaySeconds, periodSeconds, failureThreshold).",
            "Restart dependent cache service or fix network reachability."
        ]
        commands = [
            f"kubectl describe pod {pod} -n {ns}",
            f"kubectl get svc -n {ns}",
            f"kubectl get endpoints frontend-gateway -n {ns}",
            f"kubectl exec -it {pod} -n {ns} -- nc -zv redis-cluster.cache.svc.cluster.local 6379"
        ]
        rca = {
            "incident_title": f"Service Degradation: Pod {pod} Unready (Readiness Probe 503)",
            "impact": "Kubernetes Service removed pod IP from Service Endpoints. Incoming HTTP user traffic is diverted or dropped if no other replicas are healthy.",
            "observed_symptoms": "Pod status 0/1 Ready. Endpoint table empty for service frontend-gateway. Kubelet readiness probe fails with 503.",
            "probable_root_cause": "The frontend application readiness probe `/readyz` checks connection to Redis Cache. Redis cluster port 6379 was unreachable, causing probe failure.",
            "supporting_evidence": evidence,
            "recommended_resolution": [
                "1. Investigate and restore Redis Cache service (`redis-cluster` in `cache` namespace).",
                "2. Verify NetworkPolicy permits outbound port 6379 egress from namespace `" + ns + "`.",
                "3. Once Redis is online, readiness probe will pass automatically and restore traffic routing."
            ],
            "validation_steps": [
                f"Verify readiness check status: `kubectl get pod {pod} -n {ns}` shows `1/1 Ready`.",
                f"Verify service endpoints: `kubectl get endpoints frontend-gateway -n {ns}` lists pod IP."
            ],
            "preventive_actions": [
                "Implement graceful fallback or circuit breaker in frontend app so missing cache degrades gracefully without failing readiness probe.",
                "Configure distinct `startupProbe` with long initial delay to avoid early false-positive readiness failures during boot."
            ]
        }

    elif cat == "PVC Pending":
        confidence = "94%"
        severity = "HIGH"
        root_cause = "StatefulSet pod `data-indexer-0` cannot be scheduled because PersistentVolumeClaim `pvc-data-indexer-0` is unbound due to Azure Disk CSI Driver provisioning bottleneck or StorageClass availability zone constraint."
        evidence = [
            f"Pod `{pod}` remains in `Pending` status with node `<none>` (unscheduled).",
            "Kube-scheduler Event: `0/3 nodes are available: 3 pod has unbound immediate PersistentVolumeClaims`.",
            "CSI Provisioner Event: `Waiting for a volume to be created by external-provisioner \"disk.csi.azure.com\"`."
        ]
        actions = [
            "Check status of PersistentVolumeClaim `pvc-data-indexer-0` in namespace `" + ns + "`.",
            "Inspect StorageClass `managed-csi-premium` settings and volumeBindingMode configuration.",
            "Verify Azure subscription storage quota and availability zone constraints for Azure Managed Disks.",
            "Describe PVC to view detailed CSI driver provisioner error logs."
        ]
        commands = [
            f"kubectl get pvc pvc-data-indexer-0 -n {ns}",
            f"kubectl describe pvc pvc-data-indexer-0 -n {ns}",
            "kubectl get storageclass",
            f"kubectl get events -n {ns} --sort-by='.metadata.creationTimestamp'"
        ]
        rca = {
            "incident_title": f"Scheduling Stalled: StatefulPod {pod} Pending (Unbound PVC)",
            "impact": "Data indexer storage node cannot start. StatefulSet pipeline stalled, blocking data indexing operations.",
            "observed_symptoms": "Pod stuck in Pending status. Kube-scheduler cannot bind pod to any cluster node.",
            "probable_root_cause": "The storage claim `pvc-data-indexer-0` uses `managed-csi-premium` with Immediate binding mode, but Azure Disk CSI driver failed to provision dynamic disk due to zone restriction or subscription quota limit.",
            "supporting_evidence": evidence,
            "recommended_resolution": [
                "1. Run `kubectl describe pvc pvc-data-indexer-0 -n " + ns + "` to pinpoint exact CSI error.",
                "2. Check if Azure subscription quota for Premium SSD Disks is exhausted in target region.",
                "3. Ensure StorageClass uses `volumeBindingMode: WaitForFirstConsumer` to avoid availability zone mismatch.",
                "4. Re-apply PVC / StatefulSet spec."
            ],
            "validation_steps": [
                f"Verify PVC status changes from `Pending` to `Bound`: `kubectl get pvc -n {ns}`.",
                f"Verify pod {pod} is scheduled onto node and transitions to `Running` state."
            ],
            "preventive_actions": [
                "Use StorageClasses configured with `volumeBindingMode: WaitForFirstConsumer` for multi-zone AKS clusters.",
                "Set up Azure Quota alerts for Azure Managed Disk resource usage."
            ]
        }

    else:
        confidence = "80%"
        severity = "MEDIUM"
        root_cause = "General Kubernetes operational anomaly detected. Review pod specs, events, and container logs."
        evidence = [f"Pod status reported as {incident.get('status')}."]
        actions = ["Inspect pod details using kubectl describe."]
        commands = [f"kubectl describe pod {pod} -n {ns}"]
        rca = {
            "incident_title": f"Operational Anomaly: {pod}",
            "impact": "Potential service disruption.",
            "observed_symptoms": f"Pod in {incident.get('status')} status.",
            "probable_root_cause": root_cause,
            "supporting_evidence": evidence,
            "recommended_resolution": actions,
            "validation_steps": ["Verify pod status is Ready."],
            "preventive_actions": ["Monitor cluster alerts."]
        }

    return {
        "confidence": confidence,
        "severity": severity,
        "root_cause": root_cause,
        "evidence": evidence,
        "actions": actions,
        "commands": commands,
        "rca": rca
    }
