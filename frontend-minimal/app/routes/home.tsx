import { useLoaderData } from "react-router";
import type { Route } from "./+types/home";
import { getUpcomingLessons, getCompletedLessons } from "../data/dummy";
import type { Lesson } from "../data/dummy";
import LessonCard from "../components/LessonCard";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "TutorCruncher AI - Home" },
    { name: "description", content: "Your tutoring dashboard" },
  ];
}

export async function loader() {
  const [upcomingLessons, completedLessons] = await Promise.all([
    getUpcomingLessons(),
    getCompletedLessons()
  ]);
  
  return {
    upcomingLessons,
    completedLessons: completedLessons.slice(0, 3) // Show only last 3 completed
  };
}

export default function Home() {
  const { upcomingLessons, completedLessons } = useLoaderData<typeof loader>();

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Upcoming Lessons</h2>
        {upcomingLessons.length > 0 ? (
          <div className="space-y-4">
            {upcomingLessons.map((lesson: Lesson) => (
              <LessonCard key={lesson.id} lesson={lesson} />
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-lg p-6 text-center text-gray-500 max-w-[600px] mx-auto">
            No upcoming lessons scheduled
          </div>
        )}
      </div>

      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Recently Completed Lessons</h2>
        {completedLessons.length > 0 ? (
          <div className="space-y-4">
            {completedLessons.map((lesson: Lesson) => (
              <LessonCard key={lesson.id} lesson={lesson} />
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-lg p-6 text-center text-gray-500 max-w-[600px] mx-auto">
            No completed lessons yet
          </div>
        )}
      </div>
    </div>
  );
}
