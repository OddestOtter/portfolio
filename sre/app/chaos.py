import time
import random

def run_chaos_test(target_service: str, failure_type: str):
    """
    Simulates a chaos engineering test run.
    
    Args:
        target_service: The service to test (e.g., 'database', 'external_api').
        failure_type: The type of failure to simulate (e.g., 'latency', 'outage').
    """
    print(f"--- Starting Chaos Test: {target_service} with {failure_type} ---")
    
    if failure_type == 'outage':
        print(f"[SIMULATION] Simulating complete outage of {target_service}...")
        time.sleep(2)
        print(f"[SUCCESS] Outage simulated and service resilience checked.")
    elif failure_type == 'latency':
        latency = random.uniform(0.5, 2.0)
        print(f"[SIMULATION] Injecting high latency ({latency:.2f}s) to {target_service}...")
        time.sleep(latency)
        print(f"[SUCCESS] Latency test completed.")
    else:
        print(f"[WARNING] Unknown failure type: {failure_type}")
        
    print("--- Chaos Test Finished ---")
