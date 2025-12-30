"use client";
import { useData } from "@/context/DataContext";
import { useState } from "react";

export default function ProjectsPage() {
  const { projects, setProjects } = useData();
  const [name, setName] = useState("");
  const [desc, setDesc] = useState("");
  const [manager, setManager] = useState("");
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");

  const addProject = (e) => {
    e.preventDefault();
    if (!name || !manager || !start || !end) return;
    setProjects([...projects, { name, desc, manager, start, end }]);
    setName("");
    setDesc("");
    setManager("");
    setStart("");
    setEnd("");
  };

  return (
    <div>
      <h2> Projects</h2>
      <form className="row g-3 mb-3" onSubmit={addProject}>
        <div className="col-md-4">
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="form-control"
            placeholder="Project Name"
            required
          />
        </div>
        <div className="col-md-4">
          <input
            value={manager}
            onChange={(e) => setManager(e.target.value)}
            className="form-control"
            placeholder="Manager"
            required
          />
        </div>
        <div className="col-md-4">
          <input
            value={start}
            onChange={(e) => setStart(e.target.value)}
            type="date"
            className="form-control"
            required
          />
        </div>
        <div className="col-md-4">
          <input
            value={end}
            onChange={(e) => setEnd(e.target.value)}
            type="date"
            className="form-control"
            required
          />
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
          <button className="btn btn-primary">Add Project</button>
        </div>
      </form>

      <ul className="list-group">
        {projects.map((p, i) => (
          <li key={i} className="list-group-item">
            <strong>{p.name}</strong> ({p.manager}) {p.start} → {p.end} <br />
            {p.desc}
          </li>
        ))}
      </ul>
    </div>
  );
}
