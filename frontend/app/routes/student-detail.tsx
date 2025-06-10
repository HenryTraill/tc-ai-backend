import type { Route } from "./+types/student-detail";
import { Link } from "react-router";
import { students, lessons } from "../data/students";

export function meta({ params }: Route.MetaArgs) {
  const student = students.find(s => s.id === params.studentId);
  return [
    { title: `${student?.name || 'Student'} - TutorCruncher AI` },
    { name: "description", content: `Student profile for ${student?.name} - TutorCruncher AI` },
  ];
}

export default function StudentDetail({ params }: Route.ComponentProps) {
  const student = students.find(s => s.id === params.studentId);
  const studentLessons = lessons.filter(l => l.studentId === params.studentId);

  if (!student) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Student Not Found</h1>
          <Link to="/students" className="text-blue-600 hover:text-blue-800">
            ← Back to Students
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 min-h-full">
      <div className="max-w-6xl mx-auto">
        <div className="mb-6">
          <Link 
            to="/students" 
            className="inline-flex items-center text-sm font-medium text-slate-600 hover:text-slate-800"
          >
            <span className="mr-1">←</span>
            Back to Students
          </Link>
        </div>

        <div className="bg-white/80 backdrop-blur-sm border border-white/20 rounded-2xl mb-8 shadow-lg">
          <div className="px-6 py-5 border-b border-slate-200">
            <div className="flex justify-between items-center">
              <div>
                <h1 className="text-4xl font-bold text-slate-800 mb-1">{student.name}</h1>
                <p className="text-slate-600 text-lg">{student.grade}</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-slate-600">Total Lessons</p>
                <p className="text-3xl font-bold text-slate-800">{student.lessonsCompleted}</p>
              </div>
            </div>
          </div>

          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Strengths</h2>
                <div className="space-y-3">
                  {student.strengths.map((strength, index) => (
                    <div
                      key={index}
                      className="flex items-center p-3 bg-white border border-gray-200 rounded-lg"
                    >
                      <div className="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
                      <span className="text-gray-800">{strength}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Areas for Improvement</h2>
                <div className="space-y-3">
                  {student.weaknesses.map((weakness, index) => (
                    <div
                      key={index}
                      className="flex items-center p-3 bg-white border border-gray-200 rounded-lg"
                    >
                      <div className="w-2 h-2 bg-orange-500 rounded-full mr-3"></div>
                      <span className="text-gray-800">{weakness}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-gray-50 border border-gray-200 rounded-xl">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Lesson History</h2>
            <p className="text-sm text-gray-600">Complete record of tutoring sessions</p>
          </div>
          <div className="p-6">
            {studentLessons.length === 0 ? (
              <p className="text-gray-500 text-center py-8">No lessons recorded yet.</p>
            ) : (
              <div className="space-y-4">
                {studentLessons
                  .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
                  .map((lesson) => (
                    <Link
                      key={lesson.id}
                      to={`/lessons/${lesson.id}`}
                      className="block bg-white/60 backdrop-blur-sm border border-white/30 rounded-xl p-5 hover:bg-white/80 hover:shadow-lg transition-all group"
                    >
                      <div className="flex justify-between items-start mb-3">
                        <h3 className="text-lg font-semibold text-slate-800 group-hover:text-blue-600 transition-colors">{lesson.topic}</h3>
                        <span className="text-sm text-slate-600 bg-slate-100/70 px-3 py-1 rounded-full">
                          {lesson.date}
                        </span>
                      </div>
                      <div className="mb-3 flex items-center space-x-3">
                        <span className="inline-block bg-blue-100/70 text-blue-700 text-xs px-2 py-1 rounded-full">
                          {lesson.subject}
                        </span>
                        <span className="text-sm text-slate-600">{lesson.startTime}</span>
                        <span>•</span>
                        <span className="text-sm text-slate-600">{lesson.duration} minutes</span>
                      </div>
                      <p className="text-slate-700 mb-4">{lesson.notes}</p>
                      <div>
                        <h4 className="text-sm font-medium text-slate-700 mb-2">Skills Practiced</h4>
                        <div className="flex flex-wrap gap-2">
                          {lesson.skills_practiced.map((skill, index) => (
                            <span
                              key={index}
                              className="inline-block bg-slate-100/70 text-slate-700 text-xs px-2 py-1 rounded-full"
                            >
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    </Link>
                  ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}