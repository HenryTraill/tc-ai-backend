import type { Route } from "./+types/lessons";
import { students, lessons } from "../data/students";
import { LessonListItem } from "~/components/LessonListItem";

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "Lessons - TutorCruncher AI" },
    { name: "description", content: "View all lessons with TutorCruncher AI" },
  ];
}

export default function Lessons() {
  const lessonsWithStudents = lessons.map(lesson => ({
    ...lesson,
    studentName: students.find(s => s.id === lesson.studentId)?.name || 'Unknown Student'
  }));

  const sortedLessons = lessonsWithStudents.sort((a, b) =>
    new Date(b.date).getTime() - new Date(a.date).getTime()
  );

  const totalDuration = lessons.reduce((sum, lesson) => sum + lesson.duration, 0);
  const averageDuration = Math.round(totalDuration / lessons.length);

  const subjectStats = lessons.reduce((stats, lesson) => {
    stats[lesson.subject] = (stats[lesson.subject] || 0) + 1;
    return stats;
  }, {} as Record<string, number>);

  return (
    <div className="p-8 min-h-full bg-cream">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-slate-800 mb-2">Lessons ({lessons.length})</h1>
            <p className="text-slate-600 text-lg">All tutoring sessions and lesson details</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="group bg-gradient-to-br from-blue-50 to-indigo-100 border border-blue-200 rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-blue-700 uppercase tracking-wide">Total Hours</h3>
              <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <p className="text-4xl font-bold text-slate-800 mb-2 group-hover:text-blue-600 transition-colors">
              {Math.round(totalDuration / 60 * 10) / 10}
            </p>
            <div className="flex items-center">
              <p className="text-sm text-slate-600">Hours taught</p>
              <div className="ml-auto flex items-center text-green-600 text-xs">
                <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
                <span className="font-medium">Growing</span>
              </div>
            </div>
          </div>

          {/* Average Duration Card */}
          <div className="group bg-gradient-to-br from-emerald-50 to-green-100 border border-emerald-200 rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-emerald-700 uppercase tracking-wide">Avg Duration</h3>
              <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
            </div>
            <div className="flex items-baseline mb-2">
              <p className="text-4xl font-bold text-slate-800 group-hover:text-emerald-600 transition-colors">
                {averageDuration}
              </p>
              <span className="text-xl font-medium text-slate-500 ml-1">min</span>
            </div>
            <p className="text-sm text-slate-600">Per session</p>
          </div>

          {/* Subjects Card */}
          <div className="group bg-gradient-to-br from-purple-50 to-pink-100 border border-purple-200 rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-purple-700 uppercase tracking-wide">Subjects</h3>
              <div className="w-8 h-8 bg-purple-500 rounded-lg flex items-center justify-center">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
            </div>
            <div className="max-h-32 overflow-y-auto">
              {Object.entries(subjectStats)
                .sort(([, a], [, b]) => b - a)
                .map(([subject, count]) => (
                  <div key={subject} className="flex items-center justify-between py-1">
                    <div className="flex items-center">
                      <div className="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
                      <span className="text-sm text-slate-700 font-medium">{subject}</span>
                    </div>
                    <div className="flex items-center">
                      <span className="text-sm font-bold text-slate-800 bg-white px-2 py-1 rounded-lg shadow-sm">
                        {count}
                      </span>
                    </div>
                  </div>
                ))}
            </div>
            {Object.keys(subjectStats).length > 4 && (
              <div className="mt-3 pt-3 border-t border-purple-200">
                <p className="text-xs text-purple-600 font-medium">
                  {Object.keys(subjectStats).length} subjects total
                </p>
              </div>
            )}
          </div>
        </div>

        <div className="bg-white border border-black rounded-2xl shadow-sm">
          <div className="px-6 py-5 border-b border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800">All Lessons</h2>
            <p className="text-slate-600">Click on any lesson to view detailed information</p>
          </div>
          <div className="p-6">
            {sortedLessons.length === 0 ? (
              <p className="text-slate-500 text-center py-8">No lessons recorded yet.</p>
            ) : (
              <div className="space-y-4">
                {sortedLessons.map((lesson) => (
                  <LessonListItem lesson={lesson} />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}