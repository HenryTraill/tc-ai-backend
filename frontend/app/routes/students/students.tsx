import { StudentCard } from "~/components/StudentCard";
import { useState, useEffect } from "react";
import { studentsApi, lessonsApi, type Student as ApiStudent, type Lesson as ApiLesson, type Student } from "../../data/api";
import { fullName } from "~/helpers/students";
import { Button } from "~/components/ui/Button";
import type { Route } from "./+types/students";
import { useSlideOutPanel } from "~/providers/SlideOutPanelProvider";
import { StudentForm } from "~/components/forms/student";


// Transform API data to frontend format
function transformApiStudentToFrontend(apiStudent: ApiStudent, lessons: ApiLesson[]): Student {
  const studentLessons = lessons.filter(lesson => lesson.student_id === apiStudent.id);

  // Get recent lessons (this week - last 7 days)
  const oneWeekAgo = new Date();
  oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
  const recentLessons = studentLessons
    .filter(lesson => new Date(lesson.date) >= oneWeekAgo)
    .map(lesson => ({
      id: lesson.id.toString(),
      studentId: lesson.student_id.toString(),
      date: lesson.date,
      startTime: lesson.start_time,
      subject: lesson.subject,
      topic: lesson.topic,
      duration: lesson.duration,
      notes: lesson.notes,
      skills_practiced: lesson.skills_practiced,
      main_subjects_covered: lesson.main_subjects_covered,
      student_strengths_observed: lesson.student_strengths_observed,
      student_weaknesses_observed: lesson.student_weaknesses_observed,
      tutor_tips: lesson.tutor_tips,
    }));

  return {
    id: apiStudent.id.toString(),
    name: fullName(apiStudent),
    grade: apiStudent.grade,
    strengths: apiStudent.strengths,
    weaknesses: apiStudent.weaknesses,
    lessonsCompleted: apiStudent.lessons_completed,
    recentLessons,
  };
}

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

  const { openPanel } = useSlideOutPanel();

  useEffect(() => {
    async function fetchStudentsAndLessons() {
      try {
        setLoading(true);
        // Fetch both students and lessons in parallel
        const [apiStudents, allLessons] = await Promise.all([
          studentsApi.getAll(),
          lessonsApi.getAll()
        ]);

        // Transform API data to frontend format
        const transformedStudents = apiStudents.map(student =>
          transformApiStudentToFrontend(student, allLessons)
        );

        setStudents(transformedStudents);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch students');
      } finally {
        setLoading(false);
      }
    }

    fetchStudentsAndLessons();
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
    <div className="p-8 min-h-full bg-cream">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-slate-800 mb-2">Students ({students.length})</h1>
            <p className="text-slate-600 text-lg">Manage your student roster and track progress</p>
          </div>
          <Button
            onClick={() =>
              openPanel({
                title: "Edit Student",
                content: <StudentForm />,
              })
            }
            icon="plus"
          >
            Add Student
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {students.map((student) => (
            <StudentCard key={student.id} student={student} />
          ))}
        </div>
      </div>
    </div>
  );
}