import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("calendar", "routes/calendar.tsx"),
  route("lessons", "routes/lessons.tsx"),
  route("lessons/new", "routes/lesson-new.tsx"),
  route("lessons/:lessonId", "routes/lesson-detail.tsx"),
  route("lessons/:lessonId/edit", "routes/lesson-edit.tsx"),
  route("students", "routes/students.tsx"),
  route("students/:studentId", "routes/student-detail.tsx"),
] satisfies RouteConfig;
