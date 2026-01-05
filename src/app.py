from flask import Flask, jsonify
from flask_restx import Api, Resource, fields

app = Flask(__name__)

# In-memory storage (defined early for use in routes)
tasks = []


# --- Root and Health endpoints (registered before Api takes over) ---
@app.route("/")
def index():
    """Welcome message."""
    return {"message": "Welcome to the Flask Task API!", "version": "1.0"}


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "status OK!!", "task_count": len(tasks)}), 200


# Initialize Api AFTER registering app routes
api = Api(
    app,
    version="1.0",
    title="Task API",
    description="A simple Task management API",
    doc="/docs",
)

# Namespace for tasks
ns = api.namespace("api/tasks", description="Task operations")

# --- Models for Swagger documentation ---

task_model = api.model(
    "Task",
    {
        "id": fields.Integer(readonly=True, description="Task ID"),
        "title": fields.String(required=True, description="Task title"),
        "done": fields.Boolean(description="Task completion status"),
    },
)

task_input = api.model(
    "TaskInput",
    {
        "title": fields.String(required=True, description="Task title"),
        "done": fields.Boolean(description="Task completion status"),
    },
)


# --- Task CRUD with Flask-RESTX ---


@ns.route("")
class TaskList(Resource):
    @ns.doc("list_tasks", params={"done": "Filter by completion status (true/false)"})
    @ns.marshal_list_with(task_model)
    def get(self):
        """List all tasks."""
        from flask import request

        done_filter = request.args.get("done")

        if done_filter is not None:
            done_value = done_filter.lower() == "true"
            return [t for t in tasks if t["done"] == done_value]
        return tasks

    @ns.doc("create_task")
    @ns.expect(task_input)
    @ns.marshal_with(task_model, code=201)
    def post(self):
        """Create a new task."""
        data = api.payload
        task = {
            "id": len(tasks) + 1,
            "title": data["title"],
            "done": data.get("done", False),
        }
        tasks.append(task)
        return task, 201


@ns.route("/<int:task_id>")
@ns.param("task_id", "The task identifier")
@ns.response(404, "Task not found")
class TaskItem(Resource):
    @ns.doc("get_task")
    @ns.marshal_with(task_model)
    def get(self, task_id):
        """Get a task by ID."""
        task = next((t for t in tasks if t["id"] == task_id), None)
        if not task:
            api.abort(404, "Task not found")
        return task

    @ns.doc("update_task")
    @ns.expect(task_input)
    @ns.marshal_with(task_model)
    def put(self, task_id):
        """Update a task."""
        task = next((t for t in tasks if t["id"] == task_id), None)
        if not task:
            api.abort(404, "Task not found")

        data = api.payload
        if "title" in data:
            task["title"] = data["title"]
        if "done" in data:
            task["done"] = data["done"]
        return task

    @ns.doc("delete_task")
    @ns.response(200, "Task deleted")
    def delete(self, task_id):
        """Delete a task."""
        global tasks
        original_count = len(tasks)
        tasks = [t for t in tasks if t["id"] != task_id]

        if len(tasks) == original_count:
            api.abort(404, "Task not found")
        return {"message": "Task deleted"}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
