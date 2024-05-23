import json
import random
import csv

# Parameters for dataset generation
NUM_PROCESSES = 1000
MAX_SUBTASKS = 10
SERVERS = ["S1", "S2", "S3", "S4", "S5"]
ACTIONS = ["Request", "Response"]

def generate_process_id():
    return random.randint(1000, 9999)
def generate_timestamp(start=0, end=1000):
    return random.randint(start, end)

def generate_log_entry(from_server, to_server, timestamp, action, process_id):
    return {
        "from": from_server,
        "to": to_server,
        "time": timestamp,
        "action": action,
        "process_id": process_id
    }

def generate_synthetic_dataset(num_processes, max_subtasks, servers):
    logs = []
    process_ids = set() #collection of processes

    for _ in range(num_processes):
        process_id = generate_process_id() #starter process
        while process_id in process_ids:
            process_id = generate_process_id() #recreate if process already in the collection
        process_ids.add(process_id) #add to the collection

        start_server = random.choice(servers)
        start_time = generate_timestamp()
        #starting log
        logs.append(generate_log_entry("null", start_server, start_time, "Request", process_id))

        num_subtasks = random.randint(1, max_subtasks)
        current_server = start_server
        current_time = start_time

        #create log entries for each subtask worked on
        for _ in range(num_subtasks):
            next_server = random.choice([s for s in servers if s != current_server]) #random choice a (worker) server (not itself)
            next_time = generate_timestamp(current_time, current_time + 100) #generate a random time it can take for the process to be (0-100 seconds)
            logs.append(generate_log_entry(current_server, next_server, next_time, "Request", process_id))
            current_server = next_server #go to next server
            current_time = next_time

        end_time = generate_timestamp(current_time, current_time + 100)
        #last log
        logs.append(generate_log_entry(current_server, start_server, end_time, "Response", process_id))
        #returning log to null (-user)
        logs.append(generate_log_entry(start_server, "null", end_time + random.randint(1, 10), "Response", process_id))

    return logs

# Generate the dataset
synthetic_logs = generate_synthetic_dataset(NUM_PROCESSES, MAX_SUBTASKS, SERVERS)

# Save the dataset to a JSON file
with open('synthetic_logs.json', 'w') as f:
    json.dump(synthetic_logs, f, indent=4)

# Save the dataset to a CSV file
with open('synthetic_logs.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["from", "to", "time", "action", "process_id"])
    writer.writeheader()
    for log in synthetic_logs:
        log = {k: v for k, v in log.items()}  # Replace None with empty string
        writer.writerow(log)

print("dataset saved in synthetic_logs.json and synthetic_logs.csv")
