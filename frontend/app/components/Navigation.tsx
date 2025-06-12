import { Link, useLocation } from "react-router";
import { Button } from "./ui/Button";
import { useEffect, useState } from "react";
import { Logo } from "~/svgs/logo";

export function Navigation() {
  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();


  useEffect(() => {
    setMenuOpen(false);
  }, [location.pathname]);

  const isActive = (path: string) => {
    if (path === "/" && location.pathname === "/") return true;
    if (path !== "/" && location.pathname.startsWith(path)) return true;
    return false;
  };

  const navItems = [
    { path: "/", label: "Dashboard", icon: "fas fa-fw fa-chart-line" },
    { path: "/calendar", label: "Calendar", icon: "fas fa-fw fa-calendar-alt" },
    { path: "/lessons", label: "Lessons", icon: "fas fa-fw fa-book-open" },
    { path: "/students", label: "Students", icon: "fas fa-fw fa-users" },
  ];

  const settingsItems = [
    { path: "/settings", label: "Preferences", icon: "fas fa-fw fa-cog" },
    { path: "/billing", label: "Billing", icon: "fas fa-fw fa-credit-card" },
  ];

  return (
    <nav className="w-full md:w-64 bg-baby-blue border-r border-blue-200 flex flex-col md:h-full">
      <div className="p-6 border-b border-blue-200 flex justify-between">
        <Link to="/" className="flex items-center space-x-2">
          <Logo />
        </Link>
        <div className="md:hidden">
          <Button onClick={() => setMenuOpen((prev) => !prev)}>
            <span className={`${menuOpen ? "fa fa-fw fa-x" : "fa fa-fw fa-bars"}`} />
          </Button>
        </div>
      </div>

      <div className={`
    fixed top-[85px] right-0 z-40 w-full h-full bg-baby-blue shadow-lg
    transform transition-transform duration-300 ease-in-out md:transition-none
    ${menuOpen ? 'translate-x-0' : 'translate-x-full'}
    md:relative md:top-0 md:translate-x-0 md:flex md:transform-none
    flex-col flex-1
  `}
      >
        <div className="flex-1 px-4 pt-6 md:block">
          <div className="mb-6">
            <div className="space-y-1">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-3 px-3 py-2 rounded-lg text-sm transition-colors ${isActive(item.path)
                    ? "bg-white shadow-md text-navy-blue font-medium"
                    : "text-navy-blue hover:bg-white hover:text-navy-blue-75"
                    }`}
                >
                  <i className={`${item.icon} w-4`}></i>
                  <span>{item.label}</span>
                </Link>
              ))}
            </div>
          </div>
        </div>

        {/* Account Section */}
        <div className="border-t border-blue-200 p-4">
          <div className="space-y-1">
            <Link
              to="/profile"
              className="flex items-center space-x-3 px-3 py-2 rounded-lg text-sm text-slate-700 hover:bg-white/60 hover:text-blue-700"
            >
              <i className="fas fa-user w-4"></i>
              <span>Profile</span>
            </Link>
            <button className="flex items-center space-x-3 px-3 py-2 rounded-lg text-sm text-slate-700 hover:bg-white/60 hover:text-blue-700 w-full text-left">
              <i className="fas fa-sign-out-alt w-4"></i>
              <span>Sign out</span>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}