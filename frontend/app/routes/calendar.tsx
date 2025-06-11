import type { Route } from "./+types/calendar";
import { useState, useEffect } from "react";
import { studentsApi, lessonsApi, type Student, type Lesson } from "../data/api";
import Calendar from "~/components/Calendar";
import { fullName } from "~/helpers/students";

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "Calendar - TutorCruncher AI" },
    { name: "description", content: "View lessons by date with TutorCruncher AI" },
  ];
}

export default function CalendarPage() {
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
          <p className="text-slate-600">Loading calendar...</p>
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
          <h2 className="text-xl font-semibold text-slate-800 mb-2">Error loading calendar</h2>
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
    studentName: fullName(students.find(s => s.id === lesson.student_id)) || 'Unknown Student'
  }));

  return (
    <div className="p-8 min-h-full bg-cream">
      <div className="max-w-6xl mx-auto">
        <Calendar lessons={lessonsWithStudents} />
      </div>
    </div>
  )
}