import type { Route } from "./+types/lesson-detail";
import { Link } from "react-router";
import { useState, useEffect } from "react";
import { lessonsApi, studentsApi, type Lesson, type Student } from "../data/api";
import { LessonForm } from "~/components/forms/lessons";



export function meta({ params }: Route.MetaArgs) {
  return [
    { title: `New Lesson - TutorCruncher AI` },
    { name: "description", content: `Lesson details - TutorCruncher AI` },
  ];
}
export default function LessonNew({ params }: Route.ComponentProps) {
  const [students, setStudents] = useState<Student[]>([]);
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const [lessonsData, studentsData] = await Promise.all([
          lessonsApi.getById(params.lessonId),
          studentsApi.getAll()
        ]);
        setLesson(lessonsData);
        setStudents(studentsData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch data');
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading || !lesson) {
    return (
      <div className="p-8 min-h-full bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-slate-800 mx-auto mb-4"></div>
          <p className="text-slate-600">Loading lesson...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-8 min-h-full bg-cream">
      <div className="max-w-6xl mx-auto">
        <div className="mb-6 flex items-center justify-between">
          <Link
            to={`/lessons/${lesson.id}`}
            className="inline-flex items-center text-sm font-medium text-slate-600 hover:text-slate-800"
          >
            <span className="mr-1">←</span>
            Back to Lesson
          </Link>

        </div>
      </div>
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-slate-800 mb-2">Edit Lesson</h1>
          </div>
        </div>
        <LessonForm students={students} lesson={lesson} />
      </div>
    </div>)
}



