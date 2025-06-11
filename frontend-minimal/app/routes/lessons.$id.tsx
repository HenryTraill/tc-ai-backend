import { useLoaderData, Link } from "react-router";
import type { Route } from "./+types/lessons.$id";
import { getLesson } from "../data/dummy";

export function meta({ params }: Route.MetaArgs) {
  return [
    { title: `TutorCruncher AI - Lesson ${params.id}` },
    { name: "description", content: "Lesson details" },
  ];
}

export async function loader({ params }: Route.LoaderArgs) {
  const lesson = await getLesson(params.id);
  if (!lesson) {
    throw new Response("Lesson not found", { status: 404 });
  }
  return { lesson };
}

export default function LessonDetails() {
  const { lesson } = useLoaderData<typeof loader>();

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatTime = (timeStr: string) => {
    const [hours, minutes] = timeStr.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    return `${displayHour}:${minutes} ${ampm}`;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Link
          to="/lessons"
          className="text-blue-600 hover:text-blue-800 font-medium flex items-center"
        >
          ← Back to Lessons
        </Link>
        <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${lesson.status === 'upcoming'
          ? 'bg-blue-100 text-blue-800'
          : 'bg-green-100 text-green-800'
          }`}>
          {lesson.status === 'upcoming' ? 'Upcoming' : 'Completed'}
        </span>
      </div>

      {/* Start Recording Button for Upcoming Lessons */}
      {lesson.status === 'upcoming' && (
        <div className="bg-white rounded-lg p-6 border border-gray-200">
          <button className="w-full bg-red-600 hover:bg-red-700 text-white font-medium py-3 px-6 rounded-lg flex items-center justify-center space-x-2">
            <div className="w-3 h-3 bg-white rounded-full"></div>
            <span>Start Recording Lesson</span>
          </button>
        </div>
      )}

      {/* Summary */}
      <div className="bg-white rounded-lg p-6 border border-gray-200">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">{lesson.title}</h1>

        <div className="space-y-3">
          <div>
            <span className="text-gray-600">Student: </span>
            <Link
              to={`/students/${lesson.studentId}`}
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              {lesson.studentName}
            </Link>
          </div>

          <div>
            <span className="text-gray-600">Date: </span>
            <span className="font-medium">{formatDate(lesson.date)}</span>
          </div>

          <div>
            <span className="text-gray-600">Time: </span>
            <span className="font-medium">{formatTime(lesson.start_time)}</span>
          </div>

          <div>
            <span className="text-gray-600">Duration: </span>
            <span className="font-medium">{lesson.duration} minutes</span>
          </div>
        </div>
      </div>

      {/* Proposed Structure for Upcoming Lessons */}
      {lesson.status === 'upcoming' && lesson.proposedStructure && (
        <div className="bg-white rounded-lg p-6 border border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Proposed Lesson Structure</h2>
          <div className="whitespace-pre-line text-gray-700 leading-relaxed">
            {lesson.proposedStructure}
          </div>
        </div>
      )}

      {/* Completed Lesson Details */}
      {lesson.status === 'completed' && (
        <>
          {/* Summary */}
          {lesson.summary && (
            <div className="bg-white rounded-lg p-6 border border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Lesson Summary</h2>
              <p className="text-gray-700 leading-relaxed">{lesson.summary}</p>
            </div>
          )}

          {/* Strengths & Weaknesses */}
          <div className="grid md:grid-cols-2 gap-6">
            {lesson.strengths && lesson.strengths.length > 0 && (
              <div className="bg-white rounded-lg p-6 border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Student Strengths</h3>
                <ul className="space-y-2">
                  {lesson.strengths.map((strength, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-green-500 mr-2">✓</span>
                      <span className="text-gray-700">{strength}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {lesson.weaknesses && lesson.weaknesses.length > 0 && (
              <div className="bg-white rounded-lg p-6 border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Areas for Improvement</h3>
                <ul className="space-y-2">
                  {lesson.weaknesses.map((weakness, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-yellow-500 mr-2">!</span>
                      <span className="text-gray-700">{weakness}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Tutor Tips */}
          {lesson.tutorTips && lesson.tutorTips.length > 0 && (
            <div className="bg-white rounded-lg p-6 border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Tips for Teaching</h3>
              <ul className="space-y-2">
                {lesson.tutorTips.map((tip, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-blue-500 mr-2">💡</span>
                    <span className="text-gray-700">{tip}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Recording & Transcript Options */}
          <div className="bg-white rounded-lg p-6 border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Lesson Materials</h3>
            <div className="flex space-x-4">
              {lesson.hasTranscript && (
                <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg">
                  View Transcript
                </button>
              )}
              {lesson.hasRecording && (
                <button className="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg">
                  View Recording
                </button>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}