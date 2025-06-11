import { Link } from "react-router";
import type { Lesson } from "../data/dummy";

interface LessonCardProps {
  lesson: Lesson;
}

export default function LessonCard({ lesson }: LessonCardProps) {
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
    <Link to={`/lessons/${lesson.id}`} className="block">
      <div className="bg-white rounded-lg p-6 shadow-sm border border-black hover:shadow-md transition-shadow max-w-[600px] mx-auto">
        <div className="flex items-start justify-between mb-3">
          <div>
            <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${lesson.status === 'upcoming'
              ? 'bg-blue-100 text-blue-800'
              : 'bg-green-100 text-green-800'
              }`}>
              {lesson.status === 'upcoming' ? 'Upcoming' : 'Completed'}
            </span>
          </div>
        </div>

        <h3 className="text-lg font-semibold text-gray-900 mb-2">{lesson.title}</h3>

        <p className="text-gray-600 mb-3">
          with <span className="font-medium">{lesson.studentName}</span>
        </p>

        <div className="flex items-center justify-between text-sm text-gray-500">
          <span>{formatDate(lesson.date)}</span>
          <span>{formatTime(lesson.startTime)} • {lesson.duration} min</span>
        </div>
      </div>
    </Link>
  );
}