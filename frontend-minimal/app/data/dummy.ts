export interface Student {
  id: string;
  name: string;
  age: number;
  address: string;
  progress: string;
}

export interface Lesson {
  id: string;
  title: string;
  studentId: string;
  studentName: string;
  date: string;
  startTime: string;
  duration: number; // in minutes
  status: 'upcoming' | 'completed';
  proposedStructure?: string;
  summary?: string;
  strengths?: string[];
  weaknesses?: string[];
  tutorTips?: string[];
  hasTranscript?: boolean;
  hasRecording?: boolean;
}

const students: Student[] = [
  {
    id: '1',
    name: 'Emma Johnson',
    age: 16,
    address: '123 Oak Street, Springfield, IL',
    progress: 'Making excellent progress in algebra. Struggling with geometry concepts but showing improvement in problem-solving skills.'
  },
  {
    id: '2',
    name: 'Marcus Chen',
    age: 14,
    address: '456 Pine Avenue, Springfield, IL',
    progress: 'Strong foundation in mathematics. Working on advanced calculus concepts. Very motivated and asks insightful questions.'
  },
  {
    id: '3',
    name: 'Sofia Rodriguez',
    age: 17,
    address: '789 Maple Drive, Springfield, IL',
    progress: 'Preparing for SAT math section. Improved significantly in reading comprehension and analytical writing.'
  }
];

const lessons: Lesson[] = [
  {
    id: '1',
    title: 'Algebra Review Session',
    studentId: '1',
    studentName: 'Emma Johnson',
    date: '2024-12-10',
    startTime: '15:00',
    duration: 60,
    status: 'upcoming',
    proposedStructure: '1. Review homework (10 min)\n2. Practice quadratic equations (25 min)\n3. Introduction to factoring (20 min)\n4. Wrap-up and assign homework (5 min)'
  },
  {
    id: '2',
    title: 'Calculus Fundamentals',
    studentId: '2',
    studentName: 'Marcus Chen',
    date: '2024-12-11',
    startTime: '16:30',
    duration: 90,
    status: 'upcoming',
    proposedStructure: '1. Review derivatives (15 min)\n2. Introduction to integrals (45 min)\n3. Practice problems (25 min)\n4. Q&A and next steps (5 min)'
  },
  {
    id: '3',
    title: 'SAT Math Prep',
    studentId: '3',
    studentName: 'Sofia Rodriguez',
    date: '2024-12-08',
    startTime: '14:00',
    duration: 75,
    status: 'completed',
    summary: 'Focused on trigonometry and data analysis. Sofia demonstrated strong understanding of sine and cosine functions.',
    strengths: ['Quick to grasp trigonometric identities', 'Excellent at data interpretation', 'Shows persistence with challenging problems'],
    weaknesses: ['Still struggles with complex word problems', 'Needs more practice with logarithms'],
    tutorTips: ['Use more visual aids for logarithm concepts', 'Break down word problems into smaller steps', 'Encourage more practice with graphing calculator'],
    hasTranscript: true,
    hasRecording: true
  },
  {
    id: '4',
    title: 'Geometry Basics',
    studentId: '1',
    studentName: 'Emma Johnson',
    date: '2024-12-05',
    startTime: '15:00',
    duration: 60,
    status: 'completed',
    summary: 'Covered basic geometric shapes and area calculations. Emma showed good improvement in understanding perimeter vs area.',
    strengths: ['Good spatial visualization', 'Remembers formulas well', 'Asks thoughtful questions'],
    weaknesses: ['Confusion between similar formulas', 'Needs more practice with coordinate geometry'],
    tutorTips: ['Create a formula sheet for reference', 'Use more hands-on activities', 'Practice with coordinate plane exercises'],
    hasTranscript: false,
    hasRecording: true
  }
];

// Simulate API delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export async function getStudents(): Promise<Student[]> {
  await delay(300);
  return students;
}

export async function getStudent(id: string): Promise<Student | null> {
  await delay(200);
  return students.find(s => s.id === id) || null;
}

export async function getLessons(): Promise<Lesson[]> {
  await delay(400);
  return lessons;
}

export async function getLesson(id: string): Promise<Lesson | null> {
  await delay(200);
  return lessons.find(l => l.id === id) || null;
}

export async function getLessonsByStudent(studentId: string): Promise<Lesson[]> {
  await delay(300);
  return lessons.filter(l => l.studentId === studentId);
}

export async function getUpcomingLessons(): Promise<Lesson[]> {
  await delay(300);
  return lessons.filter(l => l.status === 'upcoming').sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
}

export async function getCompletedLessons(): Promise<Lesson[]> {
  await delay(300);
  return lessons.filter(l => l.status === 'completed').sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
}