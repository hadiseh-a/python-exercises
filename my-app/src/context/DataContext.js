"use client";
import { createContext, useContext, useState } from "react";

const DataContext = createContext();

export function DataProvider({ children }) {
  // دیتای نمونه
  const [members, setMembers] = useState([
    { name: "Alice", role: "Developer", email: "alice@example.com" },
    { name: "Bob", role: "Designer", email: "bob@example.com" },
    { name: "Charlie", role: "Project Manager", email: "charlie@example.com" },
  ]);

  const [projects, setProjects] = useState([
    {
      name: "Website Redesign",
      manager: "Charlie",
      start: "2025-01-01",
      end: "2025-02-28",
      desc: "Redesign company website",
    },
    {
      name: "Mobile App",
      manager: "Alice",
      start: "2025-03-01",
      end: "2025-06-30",
      desc: "Develop new mobile app",
    },
  ]);

  const [tasks, setTasks] = useState([
    {
      title: "Design Homepage",
      project: "Website Redesign",
      member: "Bob",
      deadline: "2025-01-15",
      status: "In Progress",
      desc: "Create homepage mockup",
    },
    {
      title: "Implement Login",
      project: "Mobile App",
      member: "Alice",
      deadline: "2025-03-10",
      status: "ToDo",
      desc: "Build login functionality",
    },
    {
      title: "Setup Database",
      project: "Mobile App",
      member: "Charlie",
      deadline: "2025-03-05",
      status: "Done",
      desc: "Initialize DB schema",
    },
  ]);

  return (
    <DataContext.Provider
      value={{ members, setMembers, projects, setProjects, tasks, setTasks }}
    >
      {children}
    </DataContext.Provider>
  );
}

export const useData = () => useContext(DataContext);
