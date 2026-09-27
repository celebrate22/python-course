package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"sync"
	"time"
)

// Task represents a single todo item
type Task struct {
	ID        int       `json:"id"`
	Title     string    `json:"title"`
	Completed bool      `json:"completed"`
	CreatedAt time.Time `json:"created_at"`
}

const dbFile = "todos.json"

func main() {
	// 1. Define standard CLI flags using the built-in flag package
	addFlag := flag.String("add", "", "Add a new task with the specified title")
	listFlag := flag.Bool("list", false, "List all current tasks")
	processFlag := flag.Bool("process", false, "Run concurrent worker demo to process tasks")
	
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "Standard Todo CLI & Worker Demo\n\n")
		fmt.Fprintf(os.Stderr, "Usage:\n")
		fmt.Fprintf(os.Stderr, "  %s [flags]\n\n", os.Args[0])
		fmt.Fprintf(os.Stderr, "Flags:\n")
		flag.PrintDefaults()
	}

	flag.Parse()

	// 2. Dispatch commands based on flags
	if *addFlag != "" {
		addTask(*addFlag)
		return
	}

	if *listFlag {
		listTasks()
		return
	}

	if *processFlag {
		processTasksConcurrently()
		return
	}

	// Default behavior: print usage if no matching flags are passed
	flag.Usage()
}

// loadTasks reads the JSON file into a slice of Tasks
func loadTasks() ([]Task, error) {
	if _, err := os.Stat(dbFile); os.IsNotExist(err) {
		return []Task{}, nil
	}

	data, err := os.ReadFile(dbFile)
	if err != nil {
		return nil, err
	}

	var tasks []Task
	err = json.Unmarshal(data, &tasks)
	return tasks, err
}

// saveTasks writes the slice of Tasks back to the JSON file
func saveTasks(tasks []Task) error {
	data, err := json.MarshalIndent(tasks, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(dbFile, data, 0644)
}

func addTask(title string) {
	tasks, err := loadTasks()
	if err != nil {
		fmt.Printf("Error loading tasks: %v\n", err)
		return
	}

	newID := 1
	if len(tasks) > 0 {
		newID = tasks[len(tasks)-1].ID + 1
	}

	task := Task{
		ID:        newID,
		Title:     title,
		Completed: false,
		CreatedAt: time.Now(),
	}

	tasks = append(tasks, task)
	if err := saveTasks(tasks); err != nil {
		fmt.Printf("Error saving task: %v\n", err)
		return
	}

	fmt.Printf("Added task #%d: %s\n", task.ID, task.Title)
}

func listTasks() {
	tasks, err := loadTasks()
	if err != nil {
		fmt.Printf("Error loading tasks: %v\n", err)
		return
	}

	if len(tasks) == 0 {
		fmt.Println("No tasks found.")
		return
	}

	for _, t := range tasks {
		status := " "
		if t.Completed {
			status = "X"
		}
		fmt.Printf("[%s] %d: %s\n", status, t.ID, t.Title)
	}
}

// Concurrent Worker Demo
// It spins up 3 background workers to simulation-process the current tasks.
func processTasksConcurrently() {
	tasks, err := loadTasks()
	if err != nil || len(tasks) == 0 {
		fmt.Println("No tasks to process. Add some tasks first using '--add'.")
		return
	}

	fmt.Printf("Starting concurrent processing for %d tasks...\n", len(tasks))

	taskChan := make(chan Task, len(tasks))
	var wg sync.WaitGroup

	// Start 3 concurrent worker routines
	numWorkers := 3
	for i := 1; i <= numWorkers; i++ {
		wg.Add(1)
		go worker(i, taskChan, &wg)
	}

	// Feed tasks into the channel
	for _, t := range tasks {
		taskChan <- t
	}
	close(taskChan) // Signal workers that no more tasks are coming

	wg.Wait() // Wait for all workers to finish
	fmt.Println("All tasks have been processed concurrently!")
}

func worker(id int, tasks <-chan Task, wg *sync.WaitGroup) {
	defer wg.Done()
	for t := range tasks {
		fmt.Printf("[Worker %d] Started processing task #%d: %s\n", id, t.ID, t.Title)
		// Simulate data processing time (e.g., syncing to a cloud server)
		time.Sleep(1 * time.Second)
		fmt.Printf("[Worker %d] Finished task #%d\n", id, t.ID)
	}
}
