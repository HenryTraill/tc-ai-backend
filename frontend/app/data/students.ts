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

export interface Lesson {
  id: string;
  studentId: string;
  studentName: string;
  date: string;
  startTime: string;
  subject: string;
  topic: string;
  duration: number;
  notes: string;
  skills_practiced: string[];
  main_subjects_covered: string[];
  student_strengths_observed: string[];
  student_weaknesses_observed: string[];
  tutor_tips: string[];
}