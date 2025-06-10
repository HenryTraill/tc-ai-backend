import type { Route } from "./+types/home";
import { Link } from "react-router";
import { students, lessons } from "../data/students";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Dashboard - TutorCruncher AI" },
    { name: "description", content: "Track student progress and lessons with TutorCruncher AI" },
  ];
}

export default function Home() {
  const totalStudents = students.length;
  const totalLessons = lessons.length;
  const recentLessons = lessons.slice(0, 3);

  return (
    <div className="p-8 min-h-full bg-gray-50">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-slate-800 mb-2">Dashboard</h1>
          <p className="text-slate-600 text-lg">Track your tutoring progress and student insights</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
            <h3 className="text-sm font-medium text-slate-600 mb-3">Total Students</h3>
            <p className="text-3xl font-bold text-slate-800">{totalStudents}</p>
            <p className="text-sm text-slate-500 mt-2">Active learners</p>
          </div>
          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
            <h3 className="text-sm font-medium text-slate-600 mb-3">Total Lessons</h3>
            <p className="text-3xl font-bold text-slate-800">{totalLessons}</p>
            <p className="text-sm text-slate-500 mt-2">Sessions completed</p>
          </div>
          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
            <h3 className="text-sm font-medium text-slate-600 mb-3">This Week</h3>
            <p className="text-3xl font-bold text-slate-800">5</p>
            <p className="text-sm text-slate-500 mt-2">Upcoming sessions</p>
          </div>
        </div>

        <div className="bg-white border border-gray-200 rounded-2xl shadow-sm">
          <div className="px-6 py-5 border-b border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800">Recent Lessons</h2>
            <p className="text-slate-600">Latest tutoring sessions</p>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {recentLessons.map((lesson) => {
                const student = students.find(s => s.id === lesson.studentId);
                return (
                  <Link 
                    key={lesson.id} 
                    to={`/lessons/${lesson.id}`}
                    className="block bg-gray-50 border border-gray-200 rounded-xl p-5 hover:bg-gray-100 hover:shadow-md transition-all group"
                  >
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h3 className="font-semibold text-slate-800 mb-1 group-hover:text-blue-600 transition-colors">{lesson.topic}</h3>
                        <div className="flex items-center text-sm text-slate-600 space-x-2">
                          <span className="font-medium">{student?.name}</span>
                          <span>•</span>
                          <span>{lesson.subject}</span>
                          <span>•</span>
                          <span>{lesson.date}</span>
                        </div>
                      </div>
                      <span className="text-sm text-slate-600 bg-slate-200 px-3 py-1 rounded-full">
                        {lesson.duration} min
                      </span>
                    </div>
                    <p className="text-sm text-slate-700 mb-3">{lesson.notes}</p>
                    <div className="flex flex-wrap gap-2">
                      {lesson.skills_practiced.slice(0, 3).map((skill, index) => (
                        <span
                          key={index}
                          className="inline-block bg-blue-100 text-blue-800 text-xs px-3 py-1 rounded-full"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </Link>
                );
              })}
            </div>
            <div className="mt-6 text-center">
              <Link 
                to="/lessons" 
                className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-medium hover:from-purple-700 hover:to-blue-700 transition-all"
              >
                View all lessons
                <span className="ml-2">→</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
