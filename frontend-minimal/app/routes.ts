import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("lessons", "routes/lessons.tsx"),
  route("lessons/:id", "routes/lessons.$id.tsx"),
  route("students", "routes/students.tsx"),
  route("students/:id", "routes/students.$id.tsx"),
  route("insights", "routes/insights.tsx"),
  route("settings", "routes/settings.tsx"),
] satisfies RouteConfig;
