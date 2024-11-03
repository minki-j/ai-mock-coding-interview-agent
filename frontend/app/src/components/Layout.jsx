import { Link, useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';

const Layout = ({ children }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    sessionStorage.removeItem('userId');
    navigate('/login');
  };

  return (
    <div className="min-h-screen">
      <header className="container mx-auto px-4 py-6 flex justify-between items-center">
        <Link to="/" className="no-underline">
          <h1 className="text-4xl font-black text-gray-700 uppercase tracking-wider m-0">
            AI Coding Interview Agent
          </h1>
        </Link>
        
        <div className="profile-section">
          <details className="dropdown m-0" style={{ position: 'relative' }}>
            <summary>Profile</summary>
            <div 
              className="dropdown-container" 
              style={{ 
                position: 'absolute', 
                zIndex: 1, 
                backgroundColor: 'rgba(0, 0, 0, 0.2)',
                borderRadius: '8px',
                padding: '10px',
                marginTop: '5px'
              }}
            >
              <ul>
                <li><Link to="/settings">Settings</Link></li>
                <li>
                  <button 
                    onClick={handleLogout} 
                    className="bg-transparent border-none cursor-pointer text-blue-500 underline"
                  >
                    Logout
                  </button>
                </li>
              </ul>
            </div>
          </details>
        </div>
      </header>
      <main className="container mx-auto px-4">
        {children}
      </main>
    </div>
  );
};

Layout.propTypes = {
  children: PropTypes.node.isRequired
};

export default Layout;
