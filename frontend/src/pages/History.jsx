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
      <div className="max-w-md mx-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Interview History</h2>
          <button
            onClick={handleDeleteAll}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md transition-colors duration-200 flex items-center gap-2 text-sm font-medium"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                clipRule="evenodd"
              />
            </svg>
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
                <div className="flex flex-col gap-2">
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
    </div>
  );
};

export default History;
