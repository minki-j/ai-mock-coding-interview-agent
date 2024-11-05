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
      <header className="container mx-auto px-4 py-6 flex items-center justify-center gap-4">
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
            <div className="cursor-pointer px-4 py-2 rounded-lg hover:bg-gray-100 flex items-center gap-2 border border-gray-200 shadow-sm transition-all duration-200 hover:shadow-md">
              <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <span className="font-medium text-gray-700">Menu</span>
            </div>
            {isDropdownOpen && (
              <div className="absolute right-0 top-full pt-2 z-50">
                <div className="invisible-padding absolute inset-0 -left-4 -right-4 -bottom-4" />
                <div className="dropdown-container relative w-30 bg-white rounded-lg shadow-lg py-1 border border-gray-100">
                  <ul className="divide-y divide-gray-100">
                    <li>
                      <Link to="/settings" className="block px-4 py-2 text-gray-700 hover:bg-gray-50 text-right transition-colors duration-150">
                        Settings
                      </Link>
                    </li>
                    <li>
                      <button 
                        onClick={handleLogout} 
                        className="w-full text-right px-4 py-2 text-gray-700 hover:bg-gray-50 transition-colors duration-150"
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
      <main className="mx-auto px-4 w-full">
        {children}
      </main>
    </div>
  );
};

Layout.propTypes = {
  children: PropTypes.node.isRequired
};

export default Layout;
