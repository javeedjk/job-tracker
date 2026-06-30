import { useState } from "react";
import { createApplication, updateApplication } from "../api/applications";

const STATUS_OPTIONS = ["Applied", "Interviewing", "Offer", "Rejected", "Withdrawn"];

function ApplicationForm({ existingApp, onClose, onSaved }) {
  const [companyName, setCompanyName] = useState(existingApp?.company_name || "");
  const [roleTitle, setRoleTitle] = useState(existingApp?.role_title || "");
  const [status, setStatus] = useState(existingApp?.status || "Applied");
  const [jobUrl, setJobUrl] = useState(existingApp?.job_url || "");
  const [notes, setNotes] = useState(existingApp?.notes || "");
  const [error, setError] = useState("");

  const isEditing = !!existingApp;

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    const payload = {
      company_name: companyName,
      role_title: roleTitle,
      status,
      job_url: jobUrl || null,
      notes: notes || null,
    };

    try {
      if (isEditing) {
        await updateApplication(existingApp.id, payload);
      } else {
        await createApplication(payload);
      }
      onSaved();
    } catch (err) {
      setError("Could not save application");
    }
  }

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center px-4 z-50">
      <div className="bg-slate-800 rounded-2xl p-6 w-full max-w-md">
        <h2 className="text-xl font-bold text-white mb-4">
          {isEditing ? "Edit Application" : "Add Application"}
        </h2>

        <form onSubmit={handleSubmit} className="space-y-3">
          <div>
            <label className="block text-slate-300 text-sm mb-1">Company</label>
            <input
              type="text"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              required
              className="w-full px-3 py-2 rounded-lg bg-slate-700 text-white border border-slate-600 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-slate-300 text-sm mb-1">Role Title</label>
            <input
              type="text"
              value={roleTitle}
              onChange={(e) => setRoleTitle(e.target.value)}
              required
              className="w-full px-3 py-2 rounded-lg bg-slate-700 text-white border border-slate-600 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-slate-300 text-sm mb-1">Status</label>
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-slate-700 text-white border border-slate-600 focus:outline-none focus:border-blue-500"
            >
              {STATUS_OPTIONS.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-slate-300 text-sm mb-1">Job URL (optional)</label>
            <input
              type="text"
              value={jobUrl}
              onChange={(e) => setJobUrl(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-slate-700 text-white border border-slate-600 focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-slate-300 text-sm mb-1">Notes (optional)</label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              rows={3}
              className="w-full px-3 py-2 rounded-lg bg-slate-700 text-white border border-slate-600 focus:outline-none focus:border-blue-500"
            />
          </div>

          {error && <p className="text-red-400 text-sm">{error}</p>}

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-slate-700 hover:bg-slate-600 text-white py-2 rounded-lg"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-semibold"
            >
              {isEditing ? "Save Changes" : "Add"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default ApplicationForm;