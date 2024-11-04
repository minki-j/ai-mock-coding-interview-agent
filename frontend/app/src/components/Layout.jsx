import { Link, useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';
import { useState } from 'react';

const Layout = ({ children }) => {
  const navigate = useNavigate();

  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

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
          <div 
            className="relative m-0"
            onMouseEnter={() => setIsDropdownOpen(true)}
            onMouseLeave={() => setIsDropdownOpen(false)}
          >
            <div className="cursor-pointer px-4 py-2 rounded-lg hover:bg-gray-100 flex items-center gap-2">
              <span>Profile</span>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </div>
            {isDropdownOpen && (
              <div className="absolute right-0 top-full pt-2">
                <div className="invisible-padding absolute inset-0 -left-4 -right-4 -bottom-4" />
                <div className="dropdown-container relative w-35 bg-white rounded-lg shadow-lg py-2">
                  <ul className="divide-y divide-gray-100">
                    <li>
                      <Link to="/settings" className="block px-4 py-2 text-gray-700 hover:bg-gray-50 text-right">
                        Settings
                      </Link>
                    </li>
                    <li>
                      <button 
                        onClick={handleLogout} 
                        className="w-full text-right px-4 py-2 text-gray-700 hover:bg-gray-50"
                      >
                        Logout
                      </button>
                    </li>
                  </ul>
                </div>
              </div>
            )}
          </div>
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
