import { Link } from "react-router";
import { useState } from "react";

export default function Header() {
  const [showDropdown, setShowDropdown] = useState(false);

  return (
    <header className="w-full bg-white border-b border-black">
      <div className="px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Title */}
          <h1 className="text-xl font-semibold text-gray-900">TutorCruncher AI</h1>

          {/* Center Navbar */}
          <nav className="flex items-center space-x-8">
            <Link to="/" className="text-gray-700 hover:text-gray-900 font-medium">
              Home
            </Link>
            <Link to="/lessons" className="text-gray-700 hover:text-gray-900 font-medium">
              Lessons
            </Link>
            <Link to="/students" className="text-gray-700 hover:text-gray-900 font-medium">
              Students
            </Link>
            <Link to="/insights" className="text-gray-700 hover:text-gray-900 font-medium">
              Insights
            </Link>

            {/* Plus dropdown */}
            <div className="relative">
              <button
                onClick={() => setShowDropdown(!showDropdown)}
                className="text-gray-700 hover:text-gray-900 font-medium text-xl"
              >
                +
              </button>
              {showDropdown && (
                <div className="absolute top-full right-0 mt-1 bg-white border border-black rounded-lg shadow-lg py-2 min-w-[150px] z-10">
                  <Link
                    to="/lessons/new"
                    className="block px-4 py-2 text-gray-700 hover:bg-cream"
                    onClick={() => setShowDropdown(false)}
                  >
                    Create Lesson
                  </Link>
                  <Link
                    to="/students/new"
                    className="block px-4 py-2 text-gray-700 hover:bg-cream"
                    onClick={() => setShowDropdown(false)}
                  >
                    Create Student
                  </Link>
                </div>
              )}
            </div>
          </nav>

          {/* Settings cog */}
          <Link to="/settings" className="text-gray-700 hover:text-gray-900">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </Link>
        </div>
      </div>
    </header>
  );
}