import { useState, useEffect } from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { Upload, LayoutDashboard, FileText, Shield, Activity } from 'lucide-react';
import { healthCheck } from '../api/client';
import logoImg from '../assets/suraksha-logo.png';

export default function Layout() {
  const [llmMode, setLlmMode] = useState('mock');

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const res = await healthCheck();
        if (res.data.llm_mode) setLlmMode(res.data.llm_mode);
      } catch (err) {
        console.error("Failed to fetch health check", err);
      }
    };
    fetchHealth();
  }, []);

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <div className="sidebar-logo-icon">
              <img src={logoImg} alt="RegisterSync shield logo" />
            </div>
            <div>
              <div className="sidebar-logo-bank">Canara Bank</div>
              <div className="sidebar-logo-text">RegisterSync</div>
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
          <div className="sidebar-footer-badge" style={{ textTransform: 'uppercase' }}>
            <span className="sidebar-footer-dot" style={{ background: llmMode === 'ollama' ? 'var(--accent-blue)' : 'var(--accent-amber)' }}></span>
            {llmMode === 'ollama' ? 'Agentic Mode' : 'Mock Mode'}
          </div>
        </div>
      </aside>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
