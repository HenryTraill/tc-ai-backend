import type { Route } from "./+types/students";
import { Link } from "react-router";
import { students } from "../data/students";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Students - TutorCruncher AI" },
    { name: "description", content: "Manage your student roster with TutorCruncher AI" },
  ];
}

export default function Students() {
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
                  <span className="font-medium text-slate-800">{student.lessonsCompleted}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-600">Recent activity</span>
                  <span className="font-medium text-slate-800">{student.recentLessons.length} lessons</span>
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