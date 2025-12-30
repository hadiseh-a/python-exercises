"use client";
import { useData } from "@/context/DataContext";
import Link from "next/link";

export default function Dashboard() {
  const { members, projects, tasks } = useData();

  return (
    <div>
      <h2 className="mb-4"> Dashboard</h2>
      <div className="row g-3 mb-4">
        <div className="col-md-4">
          <div className="card text-center shadow-sm">
            <div className="card-body">
              <h5 className="card-title">Members</h5>
              <p className="card-text display-6">{members.length}</p>
              <Link href="/members" className="btn btn-outline-primary btn-sm">
                View Members
              </Link>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card text-center shadow-sm">
            <div className="card-body">
              <h5 className="card-title">Projects</h5>
              <p className="card-text display-6">{projects.length}</p>
              <Link href="/projects" className="btn btn-outline-primary btn-sm">
                View Projects
              </Link>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card text-center shadow-sm">
            <div className="card-body">
              <h5 className="card-title">Tasks</h5>
              <p className="card-text display-6">{tasks.length}</p>
              <Link href="/tasks" className="btn btn-outline-primary btn-sm">
                View Tasks
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
