import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("login", "routes/login.tsx"),
  route("calendar", "routes/calendar.tsx"),
  route("lessons", "routes/lessons/lessons.tsx"),
  route("lessons/:lessonId", "routes/lessons/lesson-detail.tsx"),
  route("students", "routes/students/students.tsx"),
  route("students/:studentId", "routes/students/student-detail.tsx"),
] satisfies RouteConfig;
