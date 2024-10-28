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
    <div>
      <h1>Login Page</h1>
      <p>Please login to continue.</p>
      <GoogleLogin
        onSuccess={handleLoginSuccess}
        onError={handleLoginFailure}
      />
    </div>
  );
};


export default Login;
