import { useEffect, useState, useRef } from "react";
import { triggerResearch, getResearch } from "../api/applications";

function ResearchModal({ app, onClose }) {
  const [status, setStatus] = useState("not_started");
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");
  const pollRef = useRef(null);

  async function startPolling() {
    pollRef.current = setInterval(async () => {
      try {
        const data = await getResearch(app.id);
        setStatus(data.research_status);

        if (data.research_status === "completed") {
          setReport(data.research_report);
          clearInterval(pollRef.current);
        } else if (data.research_status === "failed") {
          setError(data.research_report || "Research failed");
          clearInterval(pollRef.current);
        }
      } catch (err) {
        setError("Could not check research status");
        clearInterval(pollRef.current);
      }
    }, 3000); // check every 3 seconds
  }

  async function handleStart() {
    setError("");
    setStatus("in_progress");
    try {
      await triggerResearch(app.id);
      startPolling();
    } catch (err) {
      setError("Could not start research");
      setStatus("not_started");
    }
  }

  // On open, check if there's already a completed report before offering to start a new one
  useEffect(() => {
    async function checkExisting() {
      try {
        const data = await getResearch(app.id);
        setStatus(data.research_status);
        if (data.research_status === "completed") {
          setReport(data.research_report);
        } else if (data.research_status === "in_progress") {
          startPolling();
        }
      } catch (err) {
        setStatus("not_started");
      }
    }
    checkExisting();

    return () => {
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, []);

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center px-4 z-50">
      <div className="bg-slate-800 rounded-2xl p-6 w-full max-w-2xl max-h-[80vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-white">
            Research: {app.company_name}
          </h2>
          <button onClick={onClose} className="text-slate-400 hover:text-white">
            ✕
          </button>
        </div>

        {status === "not_started" && (
          <div className="text-center py-8">
            <p className="text-slate-400 mb-4">No research generated yet.</p>
            <button
              onClick={handleStart}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-semibold"
            >
              Start Research
            </button>
          </div>
        )}

        {status === "in_progress" && (
          <div className="text-center py-8">
            <p className="text-slate-400">
              Researching {app.company_name}... this takes 30-60 seconds.
            </p>
          </div>
        )}

        {status === "failed" && (
          <p className="text-red-400 text-sm">{error}</p>
        )}

        {status === "completed" && report && (
          <div className="text-slate-200 text-sm whitespace-pre-wrap leading-relaxed">
            {report}
          </div>
        )}
      </div>
    </div>
  );
}

export default ResearchModal;