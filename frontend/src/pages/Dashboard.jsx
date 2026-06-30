import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getApplications, deleteApplication } from "../api/applications";
import { logout } from "../api/auth";
import ApplicationForm from "./ApplicationForm";

function Dashboard() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editingApp, setEditingApp] = useState(null);
  const navigate = useNavigate();

  async function fetchData() {
    try {
      const data = await getApplications();
      setApplications(data);
    } catch (err) {
      setError("Could not load applications");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchData();
  }, []);

  function handleLogout() {
    logout();
    navigate("/login");
  }

  function openAddForm() {
    setEditingApp(null);
    setShowForm(true);
  }

  function openEditForm(app) {
    setEditingApp(app);
    setShowForm(true);
  }

  function closeForm() {
    setShowForm(false);
    setEditingApp(null);
  }

  function handleSaved() {
    closeForm();
    fetchData(); // refresh the list after add/edit
  }

  async function handleDelete(id) {
    const confirmed = window.confirm("Delete this application? This can't be undone.");
    if (!confirmed) return;

    try {
      await deleteApplication(id);
      fetchData(); // refresh after delete
    } catch (err) {
      alert("Could not delete application");
    }
  }

  const statusColors = {
    Applied: "bg-blue-600",
    Interviewing: "bg-yellow-600",
    Offer: "bg-green-600",
    Rejected: "bg-red-600",
    Withdrawn: "bg-slate-600",
  };

  return (
    <div className="min-h-screen bg-slate-900 px-6 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-white">My Applications</h1>
          <div className="flex gap-3">
            <button
              onClick={openAddForm}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-semibold"
            >
              + Add Application
            </button>
            <button
              onClick={handleLogout}
              className="bg-slate-700 hover:bg-slate-600 text-white px-4 py-2 rounded-lg"
            >
              Log Out
            </button>
          </div>
        </div>

        {loading && <p className="text-slate-400">Loading...</p>}
        {error && <p className="text-red-400">{error}</p>}

        {!loading && !error && applications.length === 0 && (
          <p className="text-slate-400">No applications yet. Add your first one!</p>
        )}

        {!loading && applications.length > 0 && (
          <div className="space-y-3">
            {applications.map((app) => (
              <div
                key={app.id}
                className="bg-slate-800 rounded-xl p-4 flex justify-between items-center"
              >
                <div className="cursor-pointer flex-1" onClick={() => openEditForm(app)}>
                  <h2 className="text-white font-semibold text-lg">
                    {app.company_name}
                  </h2>
                  <p className="text-slate-400 text-sm">{app.role_title}</p>
                  {app.notes && (
                    <p className="text-slate-500 text-xs mt-1">{app.notes}</p>
                  )}
                </div>

                <div className="flex items-center gap-3">
                  <span className={`${statusColors[app.status] || "bg-slate-600"} text-white text-sm px-3 py-1 rounded-full`}>
                    {app.status}
                  </span>
                  <button
                    onClick={() => openEditForm(app)}
                    className="text-slate-400 hover:text-white text-sm"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(app.id)}
                    className="text-red-400 hover:text-red-300 text-sm"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {showForm && (
        <ApplicationForm
          existingApp={editingApp}
          onClose={closeForm}
          onSaved={handleSaved}
        />
      )}
    </div>
  );
}

export default Dashboard;