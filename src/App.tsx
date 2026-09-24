import { HashRouter, NavLink, Route, Routes, useLocation } from 'react-router-dom';
import ExamBuilder from './pages/ExamBuilder';
import ExamTaking from './pages/ExamTaking';
import History from './pages/History';
import ReviewResult from './pages/ReviewResult';

function Shell() {
  const location = useLocation();
  // Navigating away mid-exam would abandon the attempt (the back-button
  // guard in ExamTaking only catches browser back/close, not these tabs),
  // so lock them while a test is actually in progress.
  const examInProgress = location.pathname.startsWith('/exam/');

  return (
    <div className="app-shell">
      <nav className="nav-tabs">
        {examInProgress ? (
          <>
            <span className="nav-disabled" aria-disabled="true">
              建立考卷
            </span>
            <span className="nav-disabled" aria-disabled="true">
              成績列表
            </span>
          </>
        ) : (
          <>
            <NavLink to="/" end className={({ isActive }) => (isActive ? 'active' : '')}>
              建立考卷
            </NavLink>
            <NavLink to="/history" className={({ isActive }) => (isActive ? 'active' : '')}>
              成績列表
            </NavLink>
          </>
        )}
      </nav>
      <Routes>
        <Route path="/" element={<ExamBuilder />} />
        <Route path="/exam/:examId" element={<ExamTaking />} />
        <Route path="/history" element={<History />} />
        <Route path="/review/:attemptId" element={<ReviewResult />} />
      </Routes>
    </div>
  );
}

export default function App() {
  return (
    <HashRouter>
      <Shell />
    </HashRouter>
  );
}
