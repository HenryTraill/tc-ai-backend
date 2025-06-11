import type { Route } from "./+types/students";
import { Link } from "react-router";
import { useState, useEffect } from "react";
import { studentsApi, type Student } from "../data/api";

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "Students - TutorCruncher AI" },
    { name: "description", content: "Manage your student roster with TutorCruncher AI" },
  ];
}

export default function Students() {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchStudents() {
      try {
        setLoading(true);
        const data = await studentsApi.getAll();
        setStudents(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch students');
      } finally {
        setLoading(false);
      }
    }

    fetchStudents();
  }, []);

  if (loading) {
    return (
      <div className="p-8 min-h-full bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-slate-800 mx-auto mb-4"></div>
          <p className="text-slate-600">Loading students...</p>
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
          <h2 className="text-xl font-semibold text-slate-800 mb-2">Error loading students</h2>
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
  return (
    <div className="p-8 min-h-full bg-gray-50">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-slate-800 mb-2">Students</h1>
            <p className="text-slate-600 text-lg">Manage your student roster and track progress</p>
          </div>
          <div className="text-sm text-slate-600 bg-white px-4 py-2 rounded-full border border-gray-200 shadow-sm">
            {students.length} total students
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {students.map((student) => (
            <Link
              key={student.id}
              to={`/students/${student.id}`}
              className="bg-white border border-gray-200 rounded-2xl hover:shadow-md transition-all duration-200 p-6 block group"
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-slate-800 group-hover:text-slate-600">
                  {student.name}
                </h3>
                <span className="text-sm text-slate-600 bg-gray-100 px-3 py-1 rounded-full">
                  {student.grade}
                </span>
              </div>

              <div className="mb-4 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-600">Lessons completed</span>
                  <span className="font-medium text-slate-800">{student.lessons_completed}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-600">Student ID</span>
                  <span className="font-medium text-slate-800">#{student.id}</span>
                </div>
              </div>

              <div className="mb-4">
                <h4 className="text-sm font-medium text-slate-700 mb-2">Strengths</h4>
                <div className="flex flex-wrap gap-1">
                  {student.strengths.slice(0, 2).map((strength, index) => (
                    <span
                      key={index}
                      className="inline-block bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full"
                    >
                      {strength}
                    </span>
                  ))}
                  {student.strengths.length > 2 && (
                    <span className="inline-block text-green-700 text-xs px-2 py-1">
                      +{student.strengths.length - 2} more
                    </span>
                  )}
                </div>
              </div>

              <div>
                <h4 className="text-sm font-medium text-slate-700 mb-2">Focus Areas</h4>
                <div className="flex flex-wrap gap-1">
                  {student.weaknesses.slice(0, 2).map((weakness, index) => (
                    <span
                      key={index}
                      className="inline-block bg-orange-100 text-orange-800 text-xs px-2 py-1 rounded-full"
                    >
                      {weakness}
                    </span>
                  ))}
                  {student.weaknesses.length > 2 && (
                    <span className="inline-block text-orange-700 text-xs px-2 py-1">
                      +{student.weaknesses.length - 2} more
                    </span>
                  )}
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}