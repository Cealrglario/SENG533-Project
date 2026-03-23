from locust import HttpUser, TaskSet, task, between

# Define tasks for Apache server
class ApacheTasks(TaskSet):
    @task(2)
    def load_index(self):
        """Load the static index.html page"""
        self.client.get("/index.html")

    @task(1)
    def load_fibonacci(self):
        """Load the dynamic PHP fibonacci script"""
        self.client.get("/fibonacci.php")

# Define tasks for Node.js server
class NodeTasks(TaskSet):
    @task(2)
    def load_index(self):
        """Load the Node.js index page"""
        self.client.get("/")

    @task(1)
    def load_fibonacci(self):
        """Load the Node.js fibonacci endpoint"""
        self.client.get("/fibonacci")

# Define Apache user - connects to Apache server on port 9000
class ApacheUser(HttpUser):
    tasks = [ApacheTasks]
    wait_time = between(1, 3)  # Simulate wait time between requests (1-3 seconds)
    host = "http://localhost:9000"  # Apache server on port 9000

# Define Node.js user - connects to Node server on port 7000
class NodeUser(HttpUser):
    tasks = [NodeTasks]
    wait_time = between(1, 3)  # Simulate wait time between requests (1-3 seconds)
    host = "http://localhost:7000"  # Node server on port 7000