import type { Route } from "./+types/home";
import { Link } from "react-router";
import { students, lessons } from "../data/students";
import { LessonListItem } from "~/components/LessonListItem";

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "Dashboard - TutorCruncher AI" },
    { name: "description", content: "Track student progress and lessons with TutorCruncher AI" },
  ];
}

export default function Home() {
  const totalStudents = students.length;
  const totalLessons = lessons.length;
  const recentLessons = lessons.slice(0, 3);

  return (
    <div className="p-8 min-h-full bg-cream">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-slate-800 mb-2">Dashboard</h1>
          <p className="text-slate-600 text-lg">Track your tutoring progress and student insights</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white border border-black rounded-2xl p-6 shadow-sm">
            <h3 className="text-sm font-medium text-slate-600 mb-3">Total Students</h3>
            <p className="text-3xl font-bold text-slate-800">{totalStudents}</p>
            <p className="text-sm text-slate-500 mt-2">Active learners</p>
          </div>
          <div className="bg-white border border-black rounded-2xl p-6 shadow-sm">
            <h3 className="text-sm font-medium text-slate-600 mb-3">Total Lessons</h3>
            <p className="text-3xl font-bold text-slate-800">{totalLessons}</p>
            <p className="text-sm text-slate-500 mt-2">Sessions completed</p>
          </div>
          <div className="bg-white border border-black rounded-2xl p-6 shadow-sm">
            <h3 className="text-sm font-medium text-slate-600 mb-3">This Week</h3>
            <p className="text-3xl font-bold text-slate-800">5</p>
            <p className="text-sm text-slate-500 mt-2">Upcoming sessions</p>
          </div>
        </div>

        <div className="bg-white border border-black rounded-2xl shadow-sm">
          <div className="px-6 py-5 border-b border-slate-200">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold text-slate-800">Recent Lessons</h2>
              <Link
                to="/lessons"
                className="inline-flex items-center bg-steel-blue px-4 py-2 text-white rounded-lg font-medium transition-all"
              >
                View all lessons
                <span className="ml-2">→</span>
              </Link>
            </div>
            <p className="text-slate-600">Latest tutoring sessions</p>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {recentLessons.map((lesson) => (
                <LessonListItem lesson={lesson} />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
