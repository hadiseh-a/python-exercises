"use client";
import { useData } from "@/context/DataContext";
import { useState } from "react";

export default function MembersPage() {
  const { members, setMembers } = useData();
  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const [email, setEmail] = useState("");

  const addMember = (e) => {
    e.preventDefault();
    if (!name || !role || !email) return;
    setMembers([...members, { name, role, email }]);
    setName("");
    setRole("");
    setEmail("");
  };

  const deleteMember = (index) => {
    setMembers(members.filter((_, i) => i !== index));
  };

  return (
    <div>
      <h2> Members</h2>
      <form className="row g-3 mb-3" onSubmit={addMember}>
        <div className="col-md-4">
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="form-control"
            placeholder="Name"
            required
          />
        </div>
        <div className="col-md-4">
          <input
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="form-control"
            placeholder="Role"
            required
          />
        </div>
        <div className="col-md-4">
          <input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            type="email"
            className="form-control"
            placeholder="Email"
            required
          />
        </div>
        <div className="col-md-12">
          <button className="btn btn-primary">Add Member</button>
        </div>
      </form>

      <ul className="list-group">
        {members.map((m, i) => (
          <li
            key={i}
            className="list-group-item d-flex justify-content-between"
          >
            <span>
              {m.name} ({m.role}) - {m.email}
            </span>
            <button
              className="btn btn-sm btn-danger"
              onClick={() => deleteMember(i)}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
