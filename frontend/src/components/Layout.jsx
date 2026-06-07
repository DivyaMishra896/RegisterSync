import { NavLink, Outlet } from 'react-router-dom';
import { Upload, LayoutDashboard, FileText, Shield, Activity } from 'lucide-react';

export default function Layout() {
  return (
    <div className="app-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <div className="sidebar-logo-icon">🛡️</div>
            <div>
              <div className="sidebar-logo-text">Suraksha</div>
              <div className="sidebar-logo-sub">Compliance AI</div>
            </div>
          </div>
        </div>

        <nav className="sidebar-nav">
          <NavLink to="/upload" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            <Upload className="nav-icon" size={20} />
            Upload Circular
          </NavLink>
          <NavLink to="/dashboard" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            <LayoutDashboard className="nav-icon" size={20} />
            Dashboard
          </NavLink>
          <NavLink to="/circulars" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            <FileText className="nav-icon" size={20} />
            Circulars
          </NavLink>
        </nav>

        <div className="sidebar-footer">
          <div className="sidebar-footer-badge">
            <span className="sidebar-footer-dot"></span>
            Mock Mode Active
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
