
let members = [];
let projects = [];
let tasks = [];


const memberName = document.getElementById("memberName");
const memberRole = document.getElementById("memberRole");
const memberEmail = document.getElementById("memberEmail");
const membersList = document.getElementById("membersList");

const projectName = document.getElementById("projectName");
const projectDesc = document.getElementById("projectDesc");
const projectManager = document.getElementById("projectManager");
const startDate = document.getElementById("startDate");
const endDate = document.getElementById("endDate");
const projectsList = document.getElementById("projectsList");

const taskTitle = document.getElementById("taskTitle");
const taskDesc = document.getElementById("taskDesc");
const taskProject = document.getElementById("taskProject");
const taskMember = document.getElementById("taskMember");
const taskDeadline = document.getElementById("taskDeadline");
const taskStatus = document.getElementById("taskStatus");
const tasksList = document.getElementById("tasksList");

const reportOutput = document.getElementById("reportOutput");

// =====================
// Helpers
// =====================
function refreshSelects() {
  projectManager.innerHTML = members.map(
    (m, i) => `<option value="${i}">${m.name}</option>`
  ).join("");

  taskMember.innerHTML = projectManager.innerHTML;

  taskProject.innerHTML = projects.map(
    (p, i) => `<option value="${i}">${p.name}</option>`
  ).join("");
}

// =====================
// Members
// =====================
function addMember() {
  if (!memberName.value) return alert("Enter member name");

  members.push({
    name: memberName.value,
    role: memberRole.value,
    email: memberEmail.value
  });

  renderMembers();
  refreshSelects();

  memberName.value = memberRole.value = memberEmail.value = "";
}

function renderMembers() {
  membersList.innerHTML = members.map(
    m => `<li class="list-group-item">${m.name} (${m.role})</li>`
  ).join("");
}

// =====================
// Projects
// =====================
function addProject() {
  if (!projectName.value) return alert("Enter project name");

  projects.push({
    name: projectName.value,
    desc: projectDesc.value,
    manager: members[projectManager.value]?.name || "-",
    start: startDate.value,
    end: endDate.value
  });

  renderProjects();
  refreshSelects();

  projectName.value = projectDesc.value = "";
}

function renderProjects() {
  projectsList.innerHTML = projects.map(
    p => `<li class="list-group-item">
            <strong>${p.name}</strong><br>
            Manager: ${p.manager}<br>
            ${p.start} → ${p.end}
          </li>`
  ).join("");
}

// =====================
// Tasks
// =====================
function addTask() {
  if (!taskTitle.value) return alert("Enter task title");

  tasks.push({
    title: taskTitle.value,
    desc: taskDesc.value,
    project: projects[taskProject.value]?.name,
    member: members[taskMember.value]?.name,
    deadline: taskDeadline.value,
    status: taskStatus.value
  });

  renderTasks();

  taskTitle.value = taskDesc.value = "";
}

function renderTasks() {
  tasksList.innerHTML = tasks.map(
    t => `<li class="list-group-item">
            <strong>${t.title}</strong><br>
            Project: ${t.project}<br>
            Assigned to: ${t.member}<br>
            Status: <span class="badge bg-${getStatusColor(t.status)}">${t.status}</span><br>
            Deadline: ${t.deadline}
          </li>`
  ).join("");
}

function getStatusColor(status) {
  if (status === "Done") return "success";
  if (status === "In Progress") return "warning";
  return "secondary";
}

// =====================
// Reports
// =====================
function showOverdue() {
  const today = new Date().toISOString().split("T")[0];

  const overdue = tasks.filter(
    t => t.deadline < today && t.status !== "Done"
  );

  reportOutput.textContent = overdue.length
    ? overdue.map(t =>
        `${t.title} | ${t.member} | ${t.project} | ${t.deadline}`
      ).join("\n")
    : "No overdue tasks 🎉";
}

function memberReport() {
  let report = "";

  members.forEach(m => {
    const mt = tasks.filter(t => t.member === m.name);
    report += `${m.name}\n`;
    report += `  ToDo: ${mt.filter(t=>t.status==="ToDo").length}\n`;
    report += `  In Progress: ${mt.filter(t=>t.status==="In Progress").length}\n`;
    report += `  Done: ${mt.filter(t=>t.status==="Done").length}\n\n`;
  });

  reportOutput.textContent = report || "No members";
}

function projectSummary() {
  let report = "";

  projects.forEach(p => {
    const pt = tasks.filter(t => t.project === p.name);
    report += `${p.name}\n`;
    report += `  Total Tasks: ${pt.length}\n`;
    report += `  Done: ${pt.filter(t=>t.status==="Done").length}\n\n`;
  });

  reportOutput.textContent = report || "No projects";
}

function generateReport() {
  let text = "PROJECT MANAGEMENT REPORT\n\n";
  text += reportOutput.textContent || "No data";

  const blob = new Blob([text], { type: "text/plain" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "project-report.txt";
  link.click();
}

// =====================
// Sample Data
// =====================
function loadSampleData() {
  members = [
    { name: "Ali Ahmadi", role: "Frontend Developer", email: "ali@test.com" },
    { name: "Sara Mohammadi", role: "Backend Developer", email: "sara@test.com" },
    { name: "Reza Karimi", role: "Project Manager", email: "reza@test.com" }
  ];

  projects = [
    {
      name: "Website Redesign",
      desc: "Redesign corporate website",
      manager: "Reza Karimi",
      start: "2025-01-01",
      end: "2025-03-01"
    },
    {
      name: "Task Management App",
      desc: "Internal system",
      manager: "Reza Karimi",
      start: "2025-02-01",
      end: "2025-04-01"
    }
  ];

  tasks = [
    {
      title: "UI Layout",
      desc: "Create main pages",
      project: "Website Redesign",
      member: "Ali Ahmadi",
      deadline: "2025-01-15",
      status: "Done"
    },
    {
      title: "REST API",
      desc: "Develop backend",
      project: "Website Redesign",
      member: "Sara Mohammadi",
      deadline: "2025-01-20",
      status: "In Progress"
    },
    {
      title: "Authentication",
      desc: "Login/Register",
      project: "Task Management App",
      member: "Sara Mohammadi",
      deadline: "2025-02-10",
      status: "ToDo"
    },
    {
      title: "Planning",
      desc: "Timeline & tasks",
      project: "Task Management App",
      member: "Reza Karimi",
      deadline: "2025-02-05",
      status: "In Progress"
    }
  ];

  renderMembers();
  renderProjects();
  refreshSelects();
  renderTasks();
}


window.onload = loadSampleData;
