import type { Route } from "./+types/lessons";
import { Link } from "react-router";
import { students, lessons } from "../data/students";

export function meta({}: Route.MetaArgs) {
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
    <div className="p-8 min-h-full bg-gray-50">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-slate-800 mb-2">Lessons</h1>
            <p className="text-slate-600 text-lg">All tutoring sessions and lesson details</p>
          </div>
          <div className="text-sm text-slate-600 bg-white px-4 py-2 rounded-full border border-gray-200 shadow-sm">
            {lessons.length} total lessons
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
            <h3 className="text-sm font-medium text-slate-600 mb-3">Total Hours</h3>
            <p className="text-3xl font-bold text-slate-800">
              {Math.round(totalDuration / 60 * 10) / 10}
            </p>
            <p className="text-sm text-slate-500 mt-2">Hours taught</p>
          </div>
          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
            <h3 className="text-sm font-medium text-slate-600 mb-3">Avg Duration</h3>
            <p className="text-3xl font-bold text-slate-800">{averageDuration} min</p>
            <p className="text-sm text-slate-500 mt-2">Per session</p>
          </div>
          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
            <h3 className="text-sm font-medium text-slate-600 mb-3">Subjects</h3>
            <div className="space-y-1">
              {Object.entries(subjectStats).map(([subject, count]) => (
                <div key={subject} className="flex justify-between">
                  <span className="text-sm text-slate-600">{subject}</span>
                  <span className="text-sm font-medium text-slate-800">{count}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-white border border-gray-200 rounded-2xl shadow-sm">
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
                  <Link
                    key={lesson.id}
                    to={`/lessons/${lesson.id}`}
                    className="block border border-gray-200 rounded-xl p-6 hover:bg-gray-50 hover:shadow-md transition-all group"
                  >
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-xl font-semibold text-slate-800 mb-1 group-hover:text-blue-600 transition-colors">
                          {lesson.topic}
                        </h3>
                        <div className="flex items-center space-x-4 text-sm text-slate-600">
                          <span className="font-medium">{lesson.studentName}</span>
                          <span>•</span>
                          <span>{lesson.subject}</span>
                          <span>•</span>
                          <span>{lesson.date}</span>
                          <span>•</span>
                          <span>{lesson.startTime}</span>
                        </div>
                      </div>
                      <span className="text-sm text-slate-600 bg-gray-100 px-3 py-1 rounded-full">
                        {lesson.duration} min
                      </span>
                    </div>
                    
                    <p className="text-slate-700 mb-4">{lesson.notes}</p>
                    
                    <div>
                      <h4 className="text-sm font-medium text-slate-700 mb-2">
                        Skills Practiced:
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {lesson.skills_practiced.map((skill, index) => (
                          <span
                            key={index}
                            className="inline-block bg-blue-100 text-blue-800 text-xs px-3 py-1 rounded-full"
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}