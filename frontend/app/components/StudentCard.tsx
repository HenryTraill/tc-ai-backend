import { Link } from "react-router";
import { Chip } from "./ui/Chip";
import type { Student } from "~/data/students";

export const StudentCard = ({ student }: { student: Student }) => (
  <Link
    key={student.id}
    to={`/students/${student.id}`}
    className="bg-white border rounded-2xl hover:shadow-xl hover:border-sky-blue transition-all duration-300 p-5 block group hover:-translate-y-1 hover:bg-cream"
  >
    <div className="flex items-center justify-between mb-4">
      <h3 className="text-lg font-bold text-navy-blue group-hover:text-sky-blue transition-colors duration-300">
        {student.name}
      </h3>
      <div className="flex items-center gap-2">
        <span className="text-sm font-bold text-navy-blue px-3 py-1.5 rounded-full border border-steel-blue">
          {student.grade}
        </span>
      </div>
    </div>

    <div className="mb-4 bg-light-blue p-4 rounded-xl border border-baby-blue">
      <div className="grid grid-cols-2 gap-4">
        <div className="text-center">
          <div className="flex items-center justify-center gap-1 mb-1">
            <svg className="w-3.5 h-3.5 text-steel-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-xs font-semibold text-steel-blue uppercase tracking-wide">Completed</span>
          </div>
          <span className="text-xl font-bold text-navy-blue">{student.lessonsCompleted}</span>
          <p className="text-xs text-slate-600">lessons</p>
        </div>
        <div className="text-center">
          <div className="flex items-center justify-center gap-1 mb-1">
            <svg className="w-3.5 h-3.5 text-steel-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
            <span className="text-xs font-semibold text-steel-blue uppercase tracking-wide">Recent</span>
          </div>
          <span className="text-xl font-bold text-navy-blue">{student?.recentLessons?.length}</span>
          <p className="text-xs text-slate-600">this week</p>
        </div>
      </div>
    </div>

    <div className="mb-4">
      <div className="flex items-center gap-2 mb-2.5">
        <svg className="w-3.5 h-3.5 text-steel-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h4 className="text-sm font-bold text-navy-blue uppercase tracking-wide">Strengths</h4>
      </div>
      <div className="flex flex-wrap gap-2">
        {student.strengths.slice(0, 2).map((strength, index) => (
          <Chip key={index} variant="strength" size="sm">
            {strength}
          </Chip>
        ))}
        {student.strengths.length > 2 && (
          <Chip variant="default" size="sm">
            +{student.strengths.length - 2} more
          </Chip>
        )}
      </div>
    </div>

    <div>
      <div className="flex items-center gap-2 mb-2.5">
        <svg className="w-3.5 h-3.5 text-steel-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h4 className="text-sm font-bold text-navy-blue uppercase tracking-wide">Focus Areas</h4>
      </div>
      <div className="flex flex-wrap gap-2">
        {student.weaknesses.slice(0, 2).map((weakness, index) => (
          <Chip key={index} variant="focus" size="sm">
            {weakness}
          </Chip>
        ))}
        {student.weaknesses.length > 2 && (
          <Chip variant="default" size="sm">
            +{student.weaknesses.length - 2} more
          </Chip>
        )}
      </div>
    </div>
  </Link>
)