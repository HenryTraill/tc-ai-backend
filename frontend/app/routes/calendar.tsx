import type { Route } from "./+types/calendar";
import { Link } from "react-router";
import { students, lessons } from "../data/students";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Calendar - TutorCruncher AI" },
    { name: "description", content: "View lessons by date with TutorCruncher AI" },
  ];
}

export default function Calendar() {
  const lessonsWithStudents = lessons.map(lesson => ({
    ...lesson,
    studentName: students.find(s => s.id === lesson.studentId)?.name || 'Unknown Student'
  }));

  const groupedLessons = lessonsWithStudents.reduce((groups, lesson) => {
    const date = lesson.date;
    if (!groups[date]) {
      groups[date] = [];
    }
    groups[date].push(lesson);
    return groups;
  }, {} as Record<string, typeof lessonsWithStudents>);

  const sortedDates = Object.keys(groupedLessons).sort((a, b) => 
    new Date(b).getTime() - new Date(a).getTime()
  );

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
    <div className="p-8 min-h-full">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-slate-800 mb-2">Calendar</h1>
            <p className="text-slate-600 text-lg">View lessons organized by date</p>
          </div>
          <div className="text-sm text-slate-600 bg-white/70 backdrop-blur-sm px-4 py-2 rounded-full border border-white/20">
            {lessons.length} total lessons
          </div>
        </div>

        {sortedDates.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-slate-500 text-lg">No lessons scheduled yet.</p>
          </div>
        ) : (
          <div className="space-y-6">
            {sortedDates.map(date => (
              <div key={date} className="bg-white/80 backdrop-blur-sm border border-white/20 rounded-2xl shadow-lg">
                <div className="px-6 py-4 border-b border-slate-200">
                  <h2 className="text-xl font-semibold text-slate-800">
                    {formatDate(date)}
                  </h2>
                  <p className="text-sm text-slate-600">
                    {groupedLessons[date].length} lesson{groupedLessons[date].length !== 1 ? 's' : ''}
                  </p>
                </div>
              <div className="p-6">
                <div className="space-y-4">
                  {groupedLessons[date].map((lesson) => (
                    <Link
                      key={lesson.id}
                      to={`/lessons/${lesson.id}`}
                      className="flex items-start p-4 border border-white/30 rounded-lg hover:bg-white/60 hover:shadow-lg transition-all group"
                    >
                      <div className="flex-shrink-0 w-2 h-2 bg-blue-500 rounded-full mt-2 mr-4"></div>
                      <div className="flex-1">
                        <div className="flex justify-between items-start mb-2">
                          <h3 className="text-lg font-semibold text-slate-800 group-hover:text-blue-600 transition-colors">
                            {lesson.topic}
                          </h3>
                          <span className="text-sm text-slate-600 bg-slate-100/70 px-2 py-1 rounded-full">
                            {lesson.duration} min
                          </span>
                        </div>
                        <p className="text-sm text-slate-600 mb-2">
                          <span className="font-medium">{lesson.studentName}</span> • {lesson.subject} • {lesson.startTime}
                        </p>
                        <p className="text-sm text-slate-700 mb-3">{lesson.notes}</p>
                        <div className="flex flex-wrap gap-2">
                          {lesson.skills_practiced.map((skill, index) => (
                            <span
                              key={index}
                              className="inline-block bg-blue-100/70 text-blue-800 text-xs px-2 py-1 rounded-full"
                            >
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}