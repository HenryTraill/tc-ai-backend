import type { Route } from "./+types/lesson-detail";
import { Link } from "react-router";
import { students, lessons } from "../data/students";

export function meta({ params }: Route.MetaArgs) {
  const lesson = lessons.find(l => l.id === params.lessonId);
  return [
    { title: `${lesson?.topic || 'Lesson'} - TutorCruncher AI` },
    { name: "description", content: `Lesson details for ${lesson?.topic} - TutorCruncher AI` },
  ];
}

export default function LessonDetail({ params }: Route.ComponentProps) {
  const lesson = lessons.find(l => l.id === params.lessonId);
  const student = lesson ? students.find(s => s.id === lesson.studentId) : null;

  if (!lesson || !student) {
    return (
      <div className="p-8 min-h-full">
        <div className="max-w-6xl mx-auto">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-slate-800 mb-4">Lesson Not Found</h1>
            <Link to="/lessons" className="text-blue-600 hover:text-blue-800">
              ← Back to Lessons
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <div className="p-8 min-h-full bg-cream">
      <div className="max-w-6xl mx-auto">
        <div className="mb-6">
          <Link
            to="/lessons"
            className="inline-flex items-center text-sm font-medium text-slate-600 hover:text-slate-800"
          >
            <span className="mr-1">←</span>
            Back to Lessons
          </Link>
        </div>

        {/* Lesson Header */}
        <div className="bg-white/80 backdrop-blur-sm border border-black rounded-2xl mb-8 shadow-lg">
          <div className="px-6 py-5 border-b border-slate-200">
            <div className="flex justify-between items-start">
              <div>
                <h1 className="text-4xl font-bold text-slate-800 mb-2">{lesson.topic}</h1>
                <div className="flex items-center space-x-4 text-slate-600">
                  <span className="text-lg">{lesson.subject}</span>
                  <span>•</span>
                  <Link
                    to={`/students/${student.id}`}
                    className="text-lg font-medium hover:text-blue-600 transition-colors"
                  >
                    {student.name}
                  </Link>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm text-slate-600 mb-1">Duration</div>
                <div className="text-2xl font-bold text-slate-800">{lesson.duration} min</div>
              </div>
            </div>
          </div>

          {/* Lesson Details */}
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              <div>
                <h3 className="text-sm font-medium text-slate-600 mb-2">Date</h3>
                <p className="text-slate-800 font-medium">{formatDate(lesson.date)}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-slate-600 mb-2">Start Time</h3>
                <p className="text-slate-800 font-medium">{lesson.startTime}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-slate-600 mb-2">Duration</h3>
                <p className="text-slate-800 font-medium">{lesson.duration} minutes</p>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-slate-800 mb-3">Session Notes</h3>
              <p className="text-slate-700 leading-relaxed">{lesson.notes}</p>
            </div>
          </div>
        </div>

        {/* Main Subjects Covered */}
        <div className="bg-white/80 backdrop-blur-sm border border-black rounded-2xl mb-8 shadow-lg">
          <div className="px-6 py-4 border-b border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800">Main Subjects Covered</h2>
            <p className="text-slate-600">Topics and concepts worked on during this lesson</p>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {lesson.main_subjects_covered.map((subject, index) => (
                <div
                  key={index}
                  className="flex items-center p-3 bg-blue-50/70 border border-blue-100 rounded-xl"
                >
                  <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                  <span className="text-slate-800">{subject}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Student Performance */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Strengths Observed */}
          <div className="bg-white/80 backdrop-blur-sm border border-black rounded-2xl shadow-lg">
            <div className="px-6 py-4 border-b border-slate-200">
              <h2 className="text-xl font-semibold text-slate-800">Student Strengths</h2>
              <p className="text-slate-600">Strengths observed during this lesson</p>
            </div>
            <div className="p-6">
              <div className="space-y-3">
                {lesson.student_strengths_observed.map((strength, index) => (
                  <div
                    key={index}
                    className="flex items-start p-4 bg-green-50/70 border border-green-100 rounded-xl"
                  >
                    <div className="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span className="text-slate-800">{strength}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Weaknesses Observed */}
          <div className="bg-white/80 backdrop-blur-sm border border-black rounded-2xl shadow-lg">
            <div className="px-6 py-4 border-b border-slate-200">
              <h2 className="text-xl font-semibold text-slate-800">Areas for Improvement</h2>
              <p className="text-slate-600">Challenges observed during this lesson</p>
            </div>
            <div className="p-6">
              <div className="space-y-3">
                {lesson.student_weaknesses_observed.map((weakness, index) => (
                  <div
                    key={index}
                    className="flex items-start p-4 bg-orange-50/70 border border-orange-100 rounded-xl"
                  >
                    <div className="w-2 h-2 bg-orange-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <span className="text-slate-800">{weakness}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Tutor Tips */}
        <div className="bg-white/80 backdrop-blur-sm border border-black rounded-2xl mb-8 shadow-lg">
          <div className="px-6 py-4 border-b border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800">Tips for Future Sessions</h2>
            <p className="text-slate-600">Recommendations for continuing with this student</p>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-2 gap-4">
              {lesson.tutor_tips.map((tip, index) => (
                <div
                  key={index}
                  className="flex items-start p-4 border border-steel-blue rounded-xl"
                >
                  <div className="w-6 h-6 bg-black rounded-full flex items-center justify-center mr-4 flex-shrink-0 mt-0.5">
                    <span className="text-white text-xs font-bold">{index + 1}</span>
                  </div>
                  <span className="text-slate-800">{tip}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Skills Practiced */}
        <div className="bg-white/80 backdrop-blur-sm border border-black rounded-2xl shadow-lg">
          <div className="px-6 py-4 border-b border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800">Skills Practiced</h2>
            <p className="text-slate-600">Specific skills worked on during this session</p>
          </div>
          <div className="p-6">
            <div className="flex flex-wrap gap-3">
              {lesson.skills_practiced.map((skill, index) => (
                <span
                  key={index}
                  className="inline-block bg-slate-100/70 text-slate-800 px-4 py-2 rounded-full text-sm font-medium"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}