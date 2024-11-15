import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const History = () => {
  const navigate = useNavigate();
  const [interviews, setInterviews] = useState([]);

  useEffect(() => {
    const user_id = sessionStorage.getItem("userId");
    if (!user_id) {
      navigate("/login");
    }
    const fetchHistory = async () => {
      const res = await fetch(`/get_history/${user_id}`);
      const data = await res.json();
      setInterviews(data);
    };
    fetchHistory();
  }, []);

  const handleDeleteAll = async () => {
    const user_id = sessionStorage.getItem("userId");
    if (!user_id) return;

    if (
      window.confirm(
        "Are you sure you want to delete all interviews? This action cannot be undone."
      )
    ) {
      const res = await fetch(`/delete_all_history/${user_id}`, {
        method: "DELETE",
      });

      if (res.ok) {
        setInterviews([]); // Clear the interviews list
      } else {
        alert("Failed to delete interviews");
      }
    }
  };

  return (
    <div className="p-4">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Interview History</h1>
        <button
          onClick={handleDeleteAll}
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
        >
          Delete All
        </button>
      </div>

      {interviews.length === 0 ? (
        <p>No interviews found</p>
      ) : (
        <ul className="space-y-4">
          {[...interviews].reverse().map((interview) => (
            <li
              key={interview.id}
              className="border p-4 rounded-lg hover:bg-gray-50 cursor-pointer"
              onClick={() => navigate(`/interview/${interview.id}`)}
            >
              <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2">
                <h2 className="font-semibold">{interview.title}</h2>
                <p className="text-gray-600 text-sm">
                  Started at {interview.start_date}
                </p>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default History;
