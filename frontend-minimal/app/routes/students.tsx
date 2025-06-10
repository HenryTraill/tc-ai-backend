import { useLoaderData } from "react-router";
import type { Route } from "./+types/students";
import { getStudents } from "../data/dummy";
import type { Student } from "../data/dummy";
import StudentCard from "../components/StudentCard";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "TutorCruncher AI - Students" },
    { name: "description", content: "Manage your students" },
  ];
}

export async function loader() {
  const students = await getStudents();
  return { students };
}

export default function Students() {
  const { students } = useLoaderData<typeof loader>();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Students</h1>
      </div>

      {/* Students List */}
      {students.length > 0 ? (
        <div className="space-y-4">
          {students.map((student: Student) => (
            <StudentCard key={student.id} student={student} />
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-lg p-6 text-center text-gray-500 max-w-[600px] mx-auto">
          No students found
        </div>
      )}
    </div>
  );
}