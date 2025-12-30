"use client";
import { useData } from "@/context/DataContext";

export default function ReportsPage() {
  const { tasks, members, projects } = useData();
  const today = new Date();
  const overdue = tasks.filter(
    (t) => new Date(t.deadline) < today && t.status !== "Done"
  );
  const closeDeadline = tasks.filter((t) => {
    const d = new Date(t.deadline);
    const diff = (d - today) / (1000 * 3600 * 24);
    return diff >= 0 && diff <= 3;
  });

  return (
    <div>
      <h2> Reports</h2>

      <h5>Overdue Tasks</h5>
      {overdue.length === 0 ? (
        <p className="text-success">No overdue tasks</p>
      ) : (
        <ul>
          {overdue.map((t, i) => (
            <li key={i}>
              {t.title} ({t.member}) - {t.deadline}
            </li>
          ))}
        </ul>
      )}

      <h5>Tasks per Member</h5>
      {members.map((m, i) => {
        const mtasks = tasks.filter((t) => t.member === m.name);
        return (
          <p key={i}>
            <strong>{m.name}</strong>: ToDo:{" "}
            {mtasks.filter((t) => t.status === "ToDo").length}, In Progress:{" "}
            {mtasks.filter((t) => t.status === "In Progress").length}, Done:{" "}
            {mtasks.filter((t) => t.status === "Done").length}
          </p>
        );
      })}

      <h5>Summary per Project</h5>
      {projects.map((p, i) => {
        const ptasks = tasks.filter((t) => t.project === p.name);
        return (
          <p key={i}>
            <strong>{p.name}</strong>: ToDo:{" "}
            {ptasks.filter((t) => t.status === "ToDo").length}, In Progress:{" "}
            {ptasks.filter((t) => t.status === "In Progress").length}, Done:{" "}
            {ptasks.filter((t) => t.status === "Done").length}
          </p>
        );
      })}

      <h5>Tasks with close deadlines (next 3 days)</h5>
      {closeDeadline.length === 0 ? (
        <p>None</p>
      ) : (
        <ul>
          {closeDeadline.map((t, i) => (
            <li key={i}>
              {t.title} ({t.member}) - {t.deadline}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
