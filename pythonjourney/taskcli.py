import os
import json
import argparse
import time
import queue
from threading import Thread

DB_FILE = "todos.json"

def load_tasks():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    with open(DB_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(title):
    tasks = load_tasks()
    new_id = 1
    if tasks:
        new_id = tasks[-1]["id"] + 1
        
    task = {
        "id": new_id,
        "title": title,
        "completed": False,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task #{task['id']}: {task['title']}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("📭 No tasks found.")
        return
        
    for t in tasks:
        status = "X" if t["completed"] else " "
        print(f"[{status}] {t['id']}: {t['title']}")

def worker(worker_id, task_queue):
    while True:
        try:
            task = task_queue.get_nowait()
        except queue.Empty:
            break
            
        print(f"[Worker {worker_id}] Started processing task #{task['id']}: {task['title']}")
        # Simulate processing overhead
        time.sleep(1)
        print(f"[Worker {worker_id}] Finished task #{task['id']}")
        task_queue.task_done()

def process_tasks_concurrently():
    tasks = load_tasks()
    if not tasks:
        print("No tasks to process. Add some tasks first using '--add'.")
        return
        
    print(f"Starting concurrent processing for {len(tasks)} tasks...")
    
    task_queue = queue.Queue()
    for task in tasks:
        task_queue.put(task)
        
    num_workers = 3
    threads = []
    
    # Fire up 3 concurrent worker threads
    for i in range(1, num_workers + 1):
        t = Thread(target=worker, args=(i, task_queue))
        t.start()
        threads.append(t)
        
    # Block main thread until workers clear the queue
    for t in threads:
        t.join()
        
    print("All tasks have been processed concurrently!")

def main():
    parser = argparse.ArgumentParser(
        description="Standard Todo CLI & Worker Demo",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--add", type=str, help="Add a new task with the specified title")
    parser.add_argument("--list", action="store_true", help="List all current tasks")
    parser.add_argument("--process", action="store_true", help="Run concurrent worker demo to process tasks")
    
    args = parser.parse_args()
    
    if args.add:
        add_task(args.add)
    elif args.list:
        list_tasks()
    elif args.process:
        process_tasks_concurrently()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
