import type { Route } from "./+types/calendar";
import Calendar from "~/components/Calendar";

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "Calendar - TutorCruncher AI" },
    { name: "description", content: "View lessons by date with TutorCruncher AI" },
  ];
}

export default function CalendarPage() {
  return (
    <div className="p-8 min-h-full bg-cream">
      <div className="max-w-6xl mx-auto">
        <Calendar />
      </div>
    </div>
  )
}