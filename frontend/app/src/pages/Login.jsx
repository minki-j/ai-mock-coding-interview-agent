import { GoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

const Login = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const userId = sessionStorage.getItem('userId');
    if (userId) {
      navigate("/");
    }
  }, [navigate]);

  const handleLoginSuccess = (response) => {
    console.log("Login Success");
    sessionStorage.setItem('userId', response.clientId);
    navigate("/");
  };

  const handleLoginFailure = (error) => {
    console.error('Login Failed:', error);
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
