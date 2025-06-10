import { Link, useLocation } from "react-router";

export function Navigation() {
  const location = useLocation();
  
  const isActive = (path: string) => {
    if (path === "/" && location.pathname === "/") return true;
    if (path !== "/" && location.pathname.startsWith(path)) return true;
    return false;
  };

  const navItems = [
    { path: "/", label: "Dashboard", icon: "📊" },
    { path: "/calendar", label: "Calendar", icon: "📅" },
    { path: "/lessons", label: "Lessons", icon: "📚" },
    { path: "/students", label: "Students", icon: "👥" },
  ];

  const settingsItems = [
    { path: "/settings", label: "Preferences", icon: "⚙️" },
    { path: "/billing", label: "Billing", icon: "💳" },
  ];

  return (
    <nav className="w-64 bg-gradient-to-br from-blue-50 to-sky-100 border-r border-blue-200 flex flex-col h-full">
      {/* Header */}
      <div className="p-6 border-b border-blue-200">
        <Link to="/" className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-lg">🎓</span>
          </div>
          <span className="text-xl font-semibold text-slate-800">TutorCruncher AI</span>
        </Link>
      </div>

      {/* Start Free Trial Banner */}
      <div className="p-4">
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white text-center py-3 px-4 rounded-lg text-sm font-medium shadow-lg">
          ✨ Start a free trial
        </div>
      </div>

      {/* Organization */}
      <div className="px-4 mb-6">
        <div className="flex items-center justify-between text-sm text-slate-600 mb-2">
          <span>Manage Organization</span>
          <button className="text-slate-500 hover:text-slate-700">
            <span>+</span>
          </button>
        </div>
        <div className="flex items-center space-x-2 text-sm">
          <span>📁</span>
          <span className="text-slate-700">Laura's Space</span>
          <button className="ml-auto text-slate-500 hover:text-slate-700">
            <span>▼</span>
          </button>
        </div>
      </div>

      {/* Main Navigation */}
      <div className="flex-1 px-4">
        <div className="mb-6">
          <div className="text-xs text-slate-600 uppercase tracking-wide mb-3 font-medium">
            Tutoring
          </div>
          <div className="space-y-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center space-x-3 px-3 py-2 rounded-lg text-sm transition-colors ${
                  isActive(item.path)
                    ? "bg-white shadow-md text-blue-700 font-medium"
                    : "text-slate-700 hover:bg-white/60 hover:text-blue-700"
                }`}
              >
                <span className="text-lg">{item.icon}</span>
                <span>{item.label}</span>
              </Link>
            ))}
          </div>
        </div>

        <div className="mb-6">
          <div className="text-xs text-slate-600 uppercase tracking-wide mb-3 font-medium">
            Settings
          </div>
          <div className="space-y-1">
            {settingsItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center space-x-3 px-3 py-2 rounded-lg text-sm transition-colors ${
                  isActive(item.path)
                    ? "bg-white shadow-md text-blue-700 font-medium"
                    : "text-slate-700 hover:bg-white/60 hover:text-blue-700"
                }`}
              >
                <span className="text-lg">{item.icon}</span>
                <span>{item.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* Account Section */}
      <div className="border-t border-blue-200 p-4">
        <div className="text-xs text-slate-600 uppercase tracking-wide mb-3 font-medium">
          Account
        </div>
        <div className="space-y-1">
          <Link
            to="/rewards"
            className="flex items-center space-x-3 px-3 py-2 rounded-lg text-sm text-slate-700 hover:bg-white/60 hover:text-blue-700"
          >
            <span className="text-lg">💎</span>
            <span>Rewards</span>
          </Link>
          <Link
            to="/profile"
            className="flex items-center space-x-3 px-3 py-2 rounded-lg text-sm text-slate-700 hover:bg-white/60 hover:text-blue-700"
          >
            <span className="text-lg">👤</span>
            <span>Profile</span>
          </Link>
          <button className="flex items-center space-x-3 px-3 py-2 rounded-lg text-sm text-slate-700 hover:bg-white/60 hover:text-blue-700 w-full text-left">
            <span className="text-lg">🚪</span>
            <span>Sign out</span>
          </button>
        </div>
      </div>
    </nav>
  );
}