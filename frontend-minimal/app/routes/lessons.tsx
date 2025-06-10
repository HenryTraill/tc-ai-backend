import { useLoaderData, useSearchParams } from "react-router";
import type { Route } from "./+types/lessons";
import { getLessons } from "../data/dummy";
import type { Lesson } from "../data/dummy";
import LessonCard from "../components/LessonCard";
import { useState } from "react";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "TutorCruncher AI - Lessons" },
    { name: "description", content: "Manage your lessons" },
  ];
}

export async function loader() {
  const lessons = await getLessons();
  return { lessons };
}

export default function Lessons() {
  const { lessons } = useLoaderData<typeof loader>();
  const [searchParams, setSearchParams] = useSearchParams();
  const [currentPage, setCurrentPage] = useState(1);
  
  const lessonType = searchParams.get('type') || 'future';
  const LESSONS_PER_PAGE = 5;

  const filteredLessons = lessons.filter(lesson => 
    lessonType === 'future' ? lesson.status === 'upcoming' : lesson.status === 'completed'
  );

  const totalPages = Math.ceil(filteredLessons.length / LESSONS_PER_PAGE);
  const startIndex = (currentPage - 1) * LESSONS_PER_PAGE;
  const paginatedLessons = filteredLessons.slice(startIndex, startIndex + LESSONS_PER_PAGE);

  const handleToggle = (type: 'future' | 'past') => {
    setSearchParams({ type });
    setCurrentPage(1);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Lessons</h1>
        
        {/* Toggle */}
        <div className="bg-white rounded-lg p-1 shadow-sm border border-gray-200">
          <button
            onClick={() => handleToggle('future')}
            className={`px-4 py-2 rounded-md font-medium transition-colors ${
              lessonType === 'future'
                ? 'bg-blue-100 text-blue-800'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Future Lessons
          </button>
          <button
            onClick={() => handleToggle('past')}
            className={`px-4 py-2 rounded-md font-medium transition-colors ${
              lessonType === 'past'
                ? 'bg-blue-100 text-blue-800'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Past Lessons
          </button>
        </div>
      </div>

      {/* Lessons List */}
      {paginatedLessons.length > 0 ? (
        <div className="space-y-4">
          {paginatedLessons.map((lesson: Lesson) => (
            <LessonCard key={lesson.id} lesson={lesson} />
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-lg p-6 text-center text-gray-500 max-w-[600px] mx-auto">
          No {lessonType === 'future' ? 'upcoming' : 'completed'} lessons found
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center items-center space-x-4 mt-8">
          <button
            onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
            disabled={currentPage === 1}
            className="px-4 py-2 bg-white border border-gray-200 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
          >
            Previous
          </button>
          
          <span className="text-gray-600">
            Page {currentPage} of {totalPages}
          </span>
          
          <button
            onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
            disabled={currentPage === totalPages}
            className="px-4 py-2 bg-white border border-gray-200 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}