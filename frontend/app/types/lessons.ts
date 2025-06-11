import type { Lesson } from "~/data/api";

export type LessonWithStudent = Lesson & {
    studentName: string;
};