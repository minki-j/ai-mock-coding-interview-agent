import { Link, useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';

const Layout = ({ children }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    sessionStorage.removeItem('userId');
    navigate('/login');
  };

  return (
    <div className="layout">
      <header className="container" style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        maxWidth: '100%',
        width: '95%'
      }}>
        <Link to="/" style={{ textDecoration: 'none' }}>
          <h1 style={{
            fontWeight: 900,
            fontSize: '2.8rem',
            color: '#4A4A4A',
            margin: 0,
            textTransform: 'uppercase',
            letterSpacing: '1px'
          }}>
            AI Coding Interview Agent
          </h1>
        </Link>
        
        <div className="profile-section">
          <details className="dropdown" style={{ margin: 0 }}>
            <summary>Profile</summary>
            <ul>
              <li><Link to="/settings">Settings</Link></li>
              <li><button onClick={handleLogout} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'blue', textDecoration: 'underline' }}>Logout</button></li>
            </ul>
          </details>
        </div>
      </header>
      <main className="container">
        {children}
      </main>
    </div>
  );
};

Layout.propTypes = {
  children: PropTypes.node.isRequired
};

export default Layout;
