import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("calendar", "routes/calendar.tsx"),
  route("lessons", "routes/lessons/lessons.tsx"),
  route("lessons/new", "routes/lessons/lesson-new.tsx"),
  route("lessons/:lessonId", "routes/lessons/lesson-detail.tsx"),
  route("lessons/:lessonId/edit", "routes/lessons/lesson-edit.tsx"),
  route("students", "routes/students/students.tsx"),
  route("students/new", "routes/students/student-new.tsx"),
  route("students/:studentId", "routes/students/student-detail.tsx"),
  route("students/:studentId/edit", "routes/students/student-edit.tsx"),
] satisfies RouteConfig;
