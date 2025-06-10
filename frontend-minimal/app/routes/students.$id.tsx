import { useLoaderData, Link } from "react-router";
import type { Route } from "./+types/students.$id";
import { getStudent, getLessonsByStudent } from "../data/dummy";
import LessonCard from "../components/LessonCard";

export function meta({ params }: Route.MetaArgs) {
  return [
    { title: `TutorCruncher AI - Student ${params.id}` },
    { name: "description", content: "Student details" },
  ];
}

export async function loader({ params }: Route.LoaderArgs) {
  const [student, lessons] = await Promise.all([
    getStudent(params.id),
    getLessonsByStudent(params.id)
  ]);
  
  if (!student) {
    throw new Response("Student not found", { status: 404 });
  }
  
  return { student, lessons };
}

export default function StudentDetails() {
  const { student, lessons } = useLoaderData<typeof loader>();

  const upcomingLessons = lessons.filter(l => l.status === 'upcoming');
  const pastLessons = lessons.filter(l => l.status === 'completed');

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Link 
          to="/students" 
          className="text-blue-600 hover:text-blue-800 font-medium flex items-center"
        >
          ← Back to Students
        </Link>
      </div>

      {/* Student Info */}
      <div className="bg-white rounded-lg p-6 border border-gray-200">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">{student.name}</h1>
        
        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-3">
            <div>
              <span className="text-gray-600 font-medium">Age: </span>
              <span>{student.age} years old</span>
            </div>
            
            <div>
              <span className="text-gray-600 font-medium">Address: </span>
              <span>{student.address}</span>
            </div>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Current Progress</h3>
            <p className="text-gray-700 leading-relaxed">{student.progress}</p>
          </div>
        </div>
      </div>

      {/* Upcoming Lessons */}
      {upcomingLessons.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Upcoming Lessons</h2>
          <div className="space-y-4">
            {upcomingLessons.map((lesson) => (
              <LessonCard key={lesson.id} lesson={lesson} />
            ))}
          </div>
        </div>
      )}

      {/* Past Lessons */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Past Lessons</h2>
        {pastLessons.length > 0 ? (
          <div className="space-y-4">
            {pastLessons.map((lesson) => (
              <LessonCard key={lesson.id} lesson={lesson} />
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-lg p-6 text-center text-gray-500 max-w-[600px] mx-auto">
            No past lessons found
          </div>
        )}
      </div>
    </div>
  );
}