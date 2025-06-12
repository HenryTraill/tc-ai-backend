import type { Route } from "./+types/lesson-detail";
import { Link, useNavigate } from "react-router";
import { useState, useEffect } from "react";
import { studentsApi, lessonsApi, type Student, type Lesson } from "../../data/api";
import { Button } from "~/components/ui/Button";
import { fullName } from "~/helpers/students";
import { DeleteModal } from "~/components/DeleteModal";


export function meta({ params }: Route.MetaArgs) {
  return [
    { title: `Lesson - TutorCruncher AI` },
    { name: "description", content: `Lesson details - TutorCruncher AI` },
  ];
}

export default function LessonDetail({ params }: Route.ComponentProps) {
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [student, setStudent] = useState<Student | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const lessonId = parseInt(params.lessonId, 10);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const lessonData = await lessonsApi.getById(lessonId);
        const studentData = await studentsApi.getById(lessonData.student_id);
        setLesson(lessonData);
        setStudent(studentData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch lesson data');
      } finally {
        setLoading(false);
      }
    }

    if (!isNaN(lessonId)) {
      fetchData();
    } else {
      setError('Invalid lesson ID');
      setLoading(false);
    }
  }, [lessonId]);

  if (loading) {
    return (
      <div className="p-8 min-h-full bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-slate-800 mx-auto mb-4"></div>
          <p className="text-slate-600">Loading lesson...</p>
        </div>
      </div>
    );
  }

  if (error || !lesson || !student) {
    return (
      <div className="p-8 min-h-full">
        <div className="max-w-6xl mx-auto">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-slate-800 mb-4">
              {error ? 'Error Loading Lesson' : 'Lesson Not Found'}
            </h1>
            {error && <p className="text-red-600 mb-4">{error}</p>}
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
        <div className="mb-6 flex items-center justify-between">
          <Link
            to="/lessons"
            className="inline-flex items-center text-sm font-medium text-slate-600 hover:text-slate-800"
          >
            <span className="mr-1">←</span>
            Back to Lessons
          </Link>
          <div className="flex gap-2">
            <Button
              variant="primary"
              href={`/lessons/${lesson.id}/edit`}
              icon="pencil"
            > Edit</Button>
            <DeleteModal
              onConfirm={() => lessonsApi.delete(lesson.id)}
              resourceName="lesson"
              redirectTo="/lessons"
            />
          </div>
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
                    {fullName(student)}
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
                <p className="text-slate-800 font-medium">{lesson.start_time}</p>
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