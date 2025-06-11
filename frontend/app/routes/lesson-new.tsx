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
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const studentsData = await studentsApi.getAll()
        setStudents(studentsData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch data');
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  return (<div className="p-8 min-h-full bg-cream">
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold text-slate-800 mb-2">Add Lesson</h1>
          <p className="text-slate-600 text-lg">All tutoring sessions and lesson details</p>
        </div>
      </div>
      <LessonForm students={students} />
    </div>
  </div>)
}



