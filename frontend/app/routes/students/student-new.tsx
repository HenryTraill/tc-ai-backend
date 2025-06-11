import type { Route } from "../+types/lesson-detail";
import { StudentForm } from "~/components/forms/student";



export function meta() {
  return [
    { title: `New Student - TutorCruncher AI` },
    { name: "description", content: `Lesson details - TutorCruncher AI` },
  ];
}
export default function StudentNew({ params }: Route.ComponentProps) {
  return (<div className="p-8 min-h-full bg-cream">
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold text-slate-800 mb-2">Add Student</h1>
        </div>
      </div>
      <StudentForm />
    </div>
  </div>)
}



