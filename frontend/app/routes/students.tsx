import type { Route } from "./+types/students";
import { Link } from "react-router";
import { students } from "../data/students";
import { StudentCard } from "~/components/StudentCard";

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "Students - TutorCruncher AI" },
    { name: "description", content: "Manage your student roster with TutorCruncher AI" },
  ];
}

export default function Students() {
  return (
    <div className="p-8 min-h-full bg-cream">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-slate-800 mb-2">Students ({students.length})</h1>
            <p className="text-slate-600 text-lg">Manage your student roster and track progress</p>
          </div>
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