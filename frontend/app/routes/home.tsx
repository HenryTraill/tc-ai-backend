import type { Route } from "./+types/home";
import { Link } from "react-router";
import { LessonListItem } from "~/components/LessonListItem";
import { useState, useEffect } from "react";
import { studentsApi, lessonsApi, type Student, type Lesson } from "../data/api";
import { StatsCard } from "~/components/StatsCard";
import { Button } from "~/components/ui/Button";

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

  const recentLessons = lessons
    .sort((a, b) => new Date(b.created_at || b.start_dt).getTime() - new Date(a.created_at || a.start_dt).getTime())
    .slice(0, 3);

  return (
    <div className="p-8 min-h-full bg-cream">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-slate-800 mb-2">Dashboard</h1>
          <p className="text-slate-600 text-lg">Track your tutoring progress and student insights</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatsCard title="Total Students" description="Active learners" value={totalStudents} trend={{
            type: "up",
            label: "In the last week"
          }} />
          <StatsCard title="Total Lessons" description="Sessions completed" value={totalLessons} trend={{
            type: "up",
            label: "In the last week"
          }} />
          <StatsCard title="This Week" description="Updcoming Sessions" value={5} trend={{
            type: "down",
            label: "In the last week"
          }} />
        </div>

        <div className="bg-white border border-black rounded-2xl shadow-sm">
          <div className="px-6 py-5 border-b border-slate-200">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold text-slate-800">Recent Lessons</h2>
              <Button
                href="/lessons"
                variant="ghost"
                icon="arrow-right"
              >
                View all lessons
              </Button>
            </div>
            <p className="text-slate-600">Latest tutoring sessions</p>
          </div >
          <div className="p-6">
            <div className="space-y-4">
              {recentLessons.map((lesson) => (
                <LessonListItem lesson={lesson} key={lesson.id} />
              ))}
            </div>
          </div>
        </div >
      </div >
    </div >
  );
}
