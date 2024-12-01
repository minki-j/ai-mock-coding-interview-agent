import { GoogleLogin } from "@react-oauth/google";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { jwtDecode } from "jwt-decode"; // TODO: install npm package

const Login = () => {
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const userId = sessionStorage.getItem("userId");
    if (userId) {
      navigate("/");
    }
  }, [navigate]);

  const handleLoginSuccess = async (response) => {
    console.log("Login Success");
    setErrorMessage("");
    const decoded = jwtDecode(response.credential);
    sessionStorage.setItem("userName", decoded.name);
    const res = await fetch("/add_user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        oauth_id: decoded.sub,
        name: decoded.name,
      }),
    });
    if (res.ok) {
      const data = await res.json();
      sessionStorage.setItem("userId", data.id);
      navigate("/");
    } else {
      setErrorMessage(
        "❌ Failed to create user account. Please try again later. If the issue persists, please report it on our GitHub repository. 🙏"
      );
    }
  };

  const handleLoginFailure = (error) => {
    console.error("Login Failed:", error);
    setErrorMessage("Login failed. Please try again.");
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] space-y-6">
      <p className="text-2xl text-black">Please login to continue.</p>
      <div className="mt-4">
        <GoogleLogin
          onSuccess={handleLoginSuccess}
          onError={handleLoginFailure}
        />
      </div>
      {errorMessage && (
        <div className="w-full max-w-md p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-600 text-sm font-medium">
            {errorMessage}
          </p>
        </div>
      )}
    </div>
  );
};

export default Login;
