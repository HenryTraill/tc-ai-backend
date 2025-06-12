import type { Lesson } from "./api";

export interface Student {
  id: string;
  first_name: string;
  last_name: string;
  grade: string;
  strengths: string[];
  weaknesses: string[];
  lessonsCompleted: number;
  recentLessons: Lesson[];
}