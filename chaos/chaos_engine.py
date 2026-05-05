import subprocess
import random
import time
import datetime
import argparse

CONTEXTS = {
    "EKS": "arn:aws:eks:us-east-1:288418346263:cluster/healer",
    "AKS": "healer-aks"
}
NAMESPACE = "default"
LABEL = "app=healer-app"

def get_pods(context):
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", NAMESPACE,
         "-l", LABEL, "--context", context,
         "-o", "jsonpath={.items[*].metadata.name}"],
        capture_output=True, text=True
    )
    return result.stdout.strip().split()

def delete_pod(pod_name, context):
    subprocess.run(
        ["kubectl", "delete", "pod", pod_name,
         "-n", NAMESPACE, "--context", context],
        capture_output=True
    )

def wait_for_recovery(context, expected=3, timeout=60):
    start = time.time()
    while time.time() - start < timeout:
        pods = get_pods(context)
        running = [p for p in pods if p]
        if len(running) >= expected:
            return time.time() - start
        time.sleep(2)
    return None

def run_chaos(cloud, context):
    print(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] Chaos on {cloud} ({context})")
    pods = get_pods(context)
    if not pods or pods == ['']:
        print(f"  No pods found on {cloud}!")
        return

    victim = random.choice(pods)
    print(f"  Deleting pod: {victim}")
    delete_pod(victim, context)

    print(f"  Waiting for recovery...")
    recovery_time = wait_for_recovery(context)

    if recovery_time:
        print(f"  Recovered in {recovery_time:.1f}s")
    else:
        print(f"  Recovery timed out!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--loop", action="store_true", help="Run continuously every 60s")
    args = parser.parse_args()

    if args.loop:
        while True:
            for cloud, ctx in CONTEXTS.items():
                run_chaos(cloud, ctx)
            print("\nSleeping 60s...\n")
            time.sleep(60)
    else:
        for cloud, ctx in CONTEXTS.items():
            run_chaos(cloud, ctx)