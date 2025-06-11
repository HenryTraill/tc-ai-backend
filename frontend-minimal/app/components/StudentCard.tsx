import { Link } from "react-router";
import type { Student } from "../data/dummy";

interface StudentCardProps {
  student: Student;
}

export default function StudentCard({ student }: StudentCardProps) {
  return (
    <Link to={`/students/${student.id}`} className="block">
      <div className="bg-white rounded-lg p-6 shadow-sm border border-black hover:shadow-md transition-shadow max-w-[600px] mx-auto">
        <div className="flex items-start justify-between mb-3">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">{student.name}</h3>
            <p className="text-gray-600">Age {student.age}</p>
          </div>
        </div>

        <p className="text-gray-600 mb-3">
          {student.address}
        </p>

        <div className="text-sm text-gray-700 bg-cream rounded-md p-3">
          <p className="font-medium mb-1">Progress Summary:</p>
          <p className="line-clamp-3">{student.progress}</p>
        </div>
      </div>
    </Link>
  );
}