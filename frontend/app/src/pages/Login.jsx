import { GoogleLogin } from "@react-oauth/google";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { jwtDecode } from "jwt-decode"; // TODO: install npm package

const Login = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const userId = sessionStorage.getItem("userId");
    if (userId) {
      navigate("/");
    }
  }, [navigate]);

  const handleLoginSuccess = async (response) => {
    console.log("Login Success");
    const decoded = jwtDecode(response.credential);
    const res = await fetch("/add_user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        oauth_id: decoded.sub,
        name: decoded.name,
      }),
    });
    const data = await res.json();
    sessionStorage.setItem("userId", data.id);
    if (res.ok) {
      navigate("/");
    }
  };

  const handleLoginFailure = (error) => {
    console.error("Login Failed:", error);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] space-y-6">
      <h1 className="text-4xl font-bold text-gray-800">Login Page</h1>
      <p className="text-lg text-gray-600">Please login to continue.</p>
      <div className="mt-4">
        <GoogleLogin
          onSuccess={handleLoginSuccess}
          onError={handleLoginFailure}
        />
      </div>
    </div>
  );
};

export default Login;
