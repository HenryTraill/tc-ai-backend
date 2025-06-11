#!/usr/bin/env python3
"""Seed the database with sample data"""

from sqlmodel import Session, select

from app.core.database import create_db_and_tables, engine
from app.models import Lesson, Student

# Sample data from frontend
students_data = [
    {
        'name': 'Emma Johnson',
        'grade': '8th Grade',
        'strengths': ['Quick learner', 'Strong in algebra', 'Good problem-solving skills'],
        'weaknesses': ['Struggles with geometry', 'Needs work on word problems'],
    },
    {
        'name': 'Marcus Chen',
        'grade': '10th Grade',
        'strengths': ['Excellent at calculus', 'Great attention to detail', 'Motivated student'],
        'weaknesses': ['Sometimes rushes through problems', 'Needs confidence building'],
    },
    {
        'name': 'Sofia Rodriguez',
        'grade': '6th Grade',
        'strengths': ['Creative thinking', 'Good at fractions', 'Eager to learn'],
        'weaknesses': ['Needs help with multiplication tables', 'Difficulty with multi-step problems'],
    },
]

lessons_data = [
    {
        'student_id': 1,
        'date': '2024-01-15',
        'start_time': '3:00 PM',
        'subject': 'Mathematics',
        'topic': 'Quadratic Equations',
        'duration': 60,
        'notes': 'Emma showed good progress with completing the square method. Still needs practice with word problems involving quadratics.',
        'skills_practiced': ['Completing the square', 'Factoring', 'Problem solving'],
        'main_subjects_covered': ['Quadratic formula', 'Completing the square', 'Word problems', 'Graphing parabolas'],
        'student_strengths_observed': [
            'Quick to understand algebraic manipulation',
            'Good visual learner',
            'Asks thoughtful questions',
        ],
        'student_weaknesses_observed': [
            'Struggles with complex word problems',
            'Sometimes rushes through steps',
            'Needs more practice with factoring',
        ],
        'tutor_tips': [
            'Use visual aids and graphing to reinforce concepts',
            'Break down word problems into smaller steps',
            'Encourage her to double-check work',
            'Practice factoring regularly',
        ],
    },
    {
        'student_id': 1,
        'date': '2024-01-08',
        'start_time': '3:00 PM',
        'subject': 'Mathematics',
        'topic': 'Linear Functions',
        'duration': 60,
        'notes': 'Great understanding of slope-intercept form. Worked on graphing linear equations.',
        'skills_practiced': ['Graphing', 'Slope calculation', 'Y-intercept'],
        'main_subjects_covered': [
            'Slope-intercept form',
            'Point-slope form',
            'Graphing linear equations',
            'Finding intercepts',
        ],
        'student_strengths_observed': [
            'Excellent graphing skills',
            'Understands coordinate system well',
            'Good with calculations',
        ],
        'student_weaknesses_observed': ['Occasionally confuses slope and y-intercept', 'Needs work on word problems'],
        'tutor_tips': [
            'Continue building on her strong graphing foundation',
            'Use real-world examples for linear relationships',
            'Practice identifying slope and intercept from graphs',
        ],
    },
    {
        'student_id': 2,
        'date': '2024-01-12',
        'start_time': '4:30 PM',
        'subject': 'Mathematics',
        'topic': 'Derivatives',
        'duration': 75,
        'notes': 'Marcus grasped the power rule quickly. Introduced chain rule concepts.',
        'skills_practiced': ['Power rule', 'Chain rule', 'Differentiation'],
        'main_subjects_covered': [
            'Power rule for differentiation',
            'Chain rule introduction',
            'Basic derivative rules',
            'Applications of derivatives',
        ],
        'student_strengths_observed': [
            'Very strong algebraic skills',
            'Grasps abstract concepts quickly',
            'Excellent problem-solving approach',
        ],
        'student_weaknesses_observed': [
            'Sometimes over-complicates simple problems',
            'Needs confidence in his abilities',
        ],
        'tutor_tips': [
            'Challenge him with complex problems to build confidence',
            'Encourage him to explain his reasoning',
            'Show multiple solution approaches',
            'Connect derivatives to real-world applications',
        ],
    },
    {
        'student_id': 3,
        'date': '2024-01-10',
        'start_time': '2:00 PM',
        'subject': 'Mathematics',
        'topic': 'Multiplication Tables',
        'duration': 45,
        'notes': 'Sofia improved her 7 and 8 times tables. Used visual aids and games to reinforce learning.',
        'skills_practiced': ['Multiplication', 'Mental math', 'Number patterns'],
        'main_subjects_covered': [
            '7 and 8 times tables',
            'Multiplication strategies',
            'Skip counting',
            'Pattern recognition',
        ],
        'student_strengths_observed': [
            'Responds well to visual learning',
            'Enjoys interactive games',
            'Good memory for patterns',
        ],
        'student_weaknesses_observed': [
            'Struggles with larger multiplication facts',
            'Needs more practice with mental math',
        ],
        'tutor_tips': [
            'Continue using games and visual aids',
            'Practice skip counting daily',
            'Use multiplication songs or rhymes',
            'Build confidence with easier facts first',
            'Celebrate small victories',
        ],
    },
]


def seed_database():
    """Seed the database with sample data"""
    print('Creating database tables...')
    create_db_and_tables()

    with Session(engine) as session:
        # Check if data already exists
        existing_students = session.exec(select(Student)).all()
        if len(existing_students) > 0:
            print('Database already contains data. Skipping seed.')
            return

        print('Seeding students...')
        students = []
        for student_data in students_data:
            student = Student(**student_data)
            session.add(student)
            students.append(student)

        session.commit()

        # Refresh to get IDs
        for student in students:
            session.refresh(student)

        print('Seeding lessons...')
        for lesson_data in lessons_data:
            lesson = Lesson(**lesson_data)
            session.add(lesson)

        session.commit()

        print('Database seeded successfully!')
        print(f'Created {len(students_data)} students and {len(lessons_data)} lessons')


if __name__ == '__main__':
    seed_database()
