import type { Route } from "./+types/home";
import { Link } from "react-router";
import { useState, useEffect } from "react";
import { studentsApi, lessonsApi, type Student, type Lesson } from "../data/api";

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "Dashboard - TutorCruncher AI" },
    { name: "description", content: "Track student progress and lessons with TutorCruncher AI" },
  ];
}

export default function Home() {
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const [lessonsData, studentsData] = await Promise.all([
          lessonsApi.getAll(),
          studentsApi.getAll()
        ]);
        setLessons(lessonsData);
        setStudents(studentsData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch data');
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="p-8 min-h-full bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-slate-800 mx-auto mb-4"></div>
          <p className="text-slate-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 min-h-full bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 mb-4">
            <svg className="h-12 w-12 mx-auto mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 18.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-slate-800 mb-2">Error loading dashboard</h2>
          <p className="text-slate-600 mb-4">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="bg-slate-800 text-white px-4 py-2 rounded-lg hover:bg-slate-700"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const totalStudents = students.length;
  const totalLessons = lessons.length;

  // Sort lessons by created_at or date and take the 3 most recent
  const recentLessons = lessons
    .sort((a, b) => new Date(b.created_at || b.date).getTime() - new Date(a.created_at || a.date).getTime())
    .slice(0, 3);

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
                const student = students.find(s => s.id === lesson.student_id);
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
