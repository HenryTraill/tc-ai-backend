import { Link } from "react-router";
import { Chip } from "./ui/Chip";
import type { Lesson } from "~/data/api";
import { formatDate, formatStudentNames, formatTime, getDurationBetween } from "~/helpers/lessons";

export const LessonListItem = ({ lesson }: { lesson: Lesson }) => {

  return (<Link
    key={lesson.id}
    to={`/lessons/${lesson.id}`}
    className="block border-2 border-slate-200 rounded-2xl p-6 bg-white hover:bg-cream hover:shadow-xl hover:border-sky-blue transition-all duration-300 group hover:-translate-y-1"
  >
    <div className="flex justify-between items-start mb-5">
      <div className="flex-1">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-3 h-3 bg-sky-blue rounded-full"></div>
          <h3 className="text-lg font-bold text-navy-blue group-hover:text-sky-blue transition-colors duration-300">
            {lesson.topic}
          </h3>
        </div>

        <div className="flex items-center flex-wrap gap-x-4 gap-y-2 text-sm">
          <div className="flex items-center gap-2">
            <svg className="w-4 h-4 text-steel-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            <span className="font-semibold text-navy-blue">
              {formatStudentNames(lesson.students)}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <svg className="w-4 h-4 text-steel-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            <span className="font-medium text-slate-700">{lesson.subject}</span>
          </div>

          <div className="flex items-center gap-2">
            <svg className="w-4 h-4 text-steel-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span className="text-slate-600">{formatDate(lesson.start_dt)}</span>
          </div>

          <div className="flex items-center gap-2">
            <svg className="w-4 h-4 text-steel-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-slate-600">{formatTime(lesson.start_dt)}</span>
          </div>
        </div>
      </div>

      <div className="ml-6 flex flex-col items-end gap-2">
        <span className="text-sm font-bold text-navy-blue bg-baby-blue px-4 py-2 rounded-full border border-sky-blue">
          {getDurationBetween(lesson.start_dt, lesson.end_dt)}
        </span>
      </div>
    </div>

    <div className="mb-5">
      <div className="bg-light-blue p-4 rounded-xl border border-baby-blue">
        <p className="text-slate-700 leading-relaxed">
          {lesson.notes}
        </p>
      </div>
    </div>

    <div>
      <div className="flex items-center gap-2 mb-3">
        <svg className="w-4 h-4 text-steel-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
        <h4 className="text-sm font-bold text-navy-blue uppercase tracking-wide">
          Skills Practiced
        </h4>
      </div>

      <div className="flex flex-wrap gap-2">
        {lesson.skills_practiced.map((skill, index) => (
          <Chip variant="default" size="sm" key={index}>
            {skill}
          </Chip>
        ))}
      </div>
    </div>
  </Link>)
}