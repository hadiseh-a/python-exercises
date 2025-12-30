"use client";
import { useData } from "@/context/DataContext";
import { useState } from "react";

export default function TasksPage() {
  const { tasks, setTasks, members, projects } = useData();
  const [title, setTitle] = useState("");
  const [project, setProject] = useState("");
  const [member, setMember] = useState("");
  const [deadline, setDeadline] = useState("");
  const [status, setStatus] = useState("ToDo");
  const [desc, setDesc] = useState("");

  const addTask = (e) => {
    e.preventDefault();
    if (!title || !project || !member || !deadline) return;
    setTasks([...tasks, { title, project, member, deadline, status, desc }]);
    setTitle("");
    setProject("");
    setMember("");
    setDeadline("");
    setStatus("ToDo");
    setDesc("");
  };

  const changeStatus = (i) => {
    const s = prompt(
      "Enter new status (ToDo / In Progress / Done):",
      tasks[i].status
    );
    if (["ToDo", "In Progress", "Done"].includes(s)) {
      const t = [...tasks];
      t[i].status = s;
      setTasks(t);
    }
  };

  const reassign = (i) => {
    const m = prompt("Enter new member:", tasks[i].member);
    if (members.find((mem) => mem.name === m)) {
      const t = [...tasks];
      t[i].member = m;
      setTasks(t);
    } else alert("Member not found");
  };

  return (
    <div>
      <h2>✅ Tasks</h2>
      <form className="row g-3 mb-3" onSubmit={addTask}>
        <div className="col-md-3">
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="form-control"
            placeholder="Task Title"
            required
          />
        </div>
        <div className="col-md-3">
          <select
            value={project}
            onChange={(e) => setProject(e.target.value)}
            className="form-select"
            required
          >
            <option value="">Select Project</option>
            {projects.map((p, i) => (
              <option key={i} value={p.name}>
                {p.name}
              </option>
            ))}
          </select>
        </div>
        <div className="col-md-3">
          <select
            value={member}
            onChange={(e) => setMember(e.target.value)}
            className="form-select"
            required
          >
            <option value="">Select Member</option>
            {members.map((m, i) => (
              <option key={i} value={m.name}>
                {m.name}
              </option>
            ))}
          </select>
        </div>
        <div className="col-md-3">
          <input
            type="date"
            value={deadline}
            onChange={(e) => setDeadline(e.target.value)}
            className="form-control"
            required
          />
        </div>
        <div className="col-md-3">
          <select
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            className="form-select"
          >
            <option>ToDo</option>
            <option>In Progress</option>
            <option>Done</option>
          </select>
        </div>
        <div className="col-md-12">
          <textarea
            value={desc}
            onChange={(e) => setDesc(e.target.value)}
            className="form-control"
            placeholder="Description"
          ></textarea>
        </div>
        <div className="col-md-12">
          <button className="btn btn-primary">Add Task</button>
        </div>
      </form>

      <ul className="list-group">
        {tasks.map((t, i) => (
          <li
            key={i}
            className="list-group-item d-flex justify-content-between align-items-center"
          >
            <div>
              <strong>{t.title}</strong> ({t.project} | {t.member}) -{" "}
              {t.deadline} <br />
              <span
                className={`badge bg-${
                  t.status === "Done"
                    ? "success"
                    : t.status === "In Progress"
                    ? "warning"
                    : "secondary"
                }`}
              >
                {t.status}
              </span>
            </div>
            <div>
              <button
                className="btn btn-sm btn-primary me-1"
                onClick={() => changeStatus(i)}
              >
                Change Status
              </button>
              <button
                className="btn btn-sm btn-secondary"
                onClick={() => reassign(i)}
              >
                Reassign
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
