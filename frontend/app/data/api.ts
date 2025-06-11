// API configuration
const API_BASE_URL = 'http://localhost:8000/api';

// Types matching backend models
export interface Student {
    id: number;
    first_name: string;
    last_name: string;
    grade: string;
    strengths: string[];
    weaknesses: string[];
    lessons_completed: number;
}

export interface StudentCreate {
    name: string;
    grade: string;
    strengths?: string[];
    weaknesses?: string[];
}

export interface StudentUpdate {
    name?: string;
    grade?: string;
    strengths?: string[];
    weaknesses?: string[];
}

export interface Lesson {
    id: number;
    student_id: number;
    date: string;
    start_time: string;
    subject: string;
    topic: string;
    duration: number;
    notes: string;
    skills_practiced: string[];
    main_subjects_covered: string[];
    student_strengths_observed: string[];
    student_weaknesses_observed: string[];
    tutor_tips: string[];
    created_at: string;
    updated_at?: string;
}

export interface LessonCreate {
    student_id: number;
    date: string;
    start_time: string;
    subject: string;
    topic: string;
    duration: number;
    notes: string;
    skills_practiced?: string[];
    main_subjects_covered?: string[];
    student_strengths_observed?: string[];
    student_weaknesses_observed?: string[];
    tutor_tips?: string[];
}

export interface LessonUpdate {
    student_id?: number;
    date?: string;
    start_time?: string;
    subject?: string;
    topic?: string;
    duration?: number;
    notes?: string;
    skills_practiced?: string[];
    main_subjects_covered?: string[];
    student_strengths_observed?: string[];
    student_weaknesses_observed?: string[];
    tutor_tips?: string[];
}

// API utility functions
class ApiError extends Error {
    constructor(public status: number, message: string) {
        super(message);
        this.name = 'ApiError';
    }
}

async function apiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;

    const response = await fetch(url, {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
        ...options,
    });

    if (!response.ok) {
        throw new ApiError(response.status, `API request failed: ${response.statusText}`);
    }

    return response.json();
}

// Student API functions
export const studentsApi = {
    getAll: (): Promise<Student[]> => apiRequest('/students'),

    getById: (id: number): Promise<Student> => apiRequest(`/students/${id}`),

    create: (student: StudentCreate): Promise<Student> =>
        apiRequest('/students', {
            method: 'POST',
            body: JSON.stringify(student),
        }),

    update: (id: number, student: StudentUpdate): Promise<Student> =>
        apiRequest(`/students/${id}`, {
            method: 'PUT',
            body: JSON.stringify(student),
        }),

    delete: (id: number): Promise<{ message: string }> =>
        apiRequest(`/students/${id}`, { method: 'DELETE' }),
};

// Lesson API functions
export const lessonsApi = {
    getAll: (studentId?: number): Promise<Lesson[]> => {
        const endpoint = studentId ? `/lessons?student_id=${studentId}` : '/lessons';
        return apiRequest(endpoint);
    },

    getById: (id: number): Promise<Lesson> => apiRequest(`/lessons/${id}`),

    getByStudent: (studentId: number): Promise<Lesson[]> =>
        apiRequest(`/lessons/student/${studentId}`),

    create: (lesson: LessonCreate): Promise<Lesson> =>
        apiRequest('/lessons', {
            method: 'POST',
            body: JSON.stringify(lesson),
        }),

    update: (id: number, lesson: LessonUpdate): Promise<Lesson> =>
        apiRequest(`/lessons/${id}`, {
            method: 'PUT',
            body: JSON.stringify(lesson),
        }),

    delete: (id: number): Promise<{ message: string }> =>
        apiRequest(`/lessons/${id}`, { method: 'DELETE' }),
}; 