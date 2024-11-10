import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';

import Home from './pages/Home';
import Interview from './pages/Interview';
import Login from './pages/Login';
import Layout from './components/Layout';
import Settings from './pages/Settings';
import History from './pages/History';
function ProtectedRoutes() {
  const userId = sessionStorage.getItem('userId');
  return userId ? <Outlet /> : <Navigate to="/login" />;
}

function App() {

  return (
    <Router>
      <Layout>
        <Routes>
          <Route element={<ProtectedRoutes/>}>
            <Route path="/" element={<Home />} />
            <Route path="/interview/:id" element={<Interview />} />
            <Route path="/history" element={<History />} />
            <Route path="/settings" element={<Settings />} />
          </Route>
          <Route path="/login" element={<Login />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
