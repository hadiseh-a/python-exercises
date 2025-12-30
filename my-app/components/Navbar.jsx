"use client";
import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark px-4">
      <Link className="navbar-brand fw-bold" href="/">
        📊 PMS
      </Link>

      <div className="navbar-nav">
        <Link className="nav-link" href="/">Dashboard</Link>
        <Link className="nav-link" href="/members">Members</Link>
        <Link className="nav-link" href="/projects">Projects</Link>
        <Link className="nav-link" href="/tasks">Tasks</Link>
        <Link className="nav-link" href="/reports">Reports</Link>
      </div>
    </nav>
  );
}
