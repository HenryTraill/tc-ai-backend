import type { Route } from "./+types/lessons";
import { Link } from "react-router";
import { useState, useEffect } from "react";
import { studentsApi, lessonsApi, type Student, type Lesson } from "../data/api";

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "Lessons - TutorCruncher AI" },
    { name: "description", content: "View all lessons with TutorCruncher AI" },
  ];
}

type LessonWithStudent = Lesson & {
  studentName: string;
};

export default function Lessons() {
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
          <p className="text-slate-600">Loading lessons...</p>
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
          <h2 className="text-xl font-semibold text-slate-800 mb-2">Error loading lessons</h2>
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

  const lessonsWithStudents: LessonWithStudent[] = lessons.map(lesson => ({
    ...lesson,
    studentName: students.find(s => s.id === lesson.student_id)?.name || 'Unknown Student'
  }));

  const sortedLessons = lessonsWithStudents.sort((a, b) =>
    new Date(b.date).getTime() - new Date(a.date).getTime()
  );

  const totalDuration = lessons.reduce((sum, lesson) => sum + lesson.duration, 0);
  const averageDuration = lessons.length > 0 ? Math.round(totalDuration / lessons.length) : 0;

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
                          <span>{lesson.start_time}</span>
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