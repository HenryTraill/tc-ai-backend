#!/usr/bin/env python3
"""Seed the database with sample data"""

import random
from datetime import datetime, timedelta

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

# Lesson templates with different topics and grades
lesson_templates = {
    '6th Grade': [
        {
            'subject': 'Mathematics',
            'topic': 'Multiplication Tables',
            'skills_practiced': ['Multiplication', 'Mental math', 'Number patterns'],
            'main_subjects_covered': [
                'Times tables',
                'Multiplication strategies',
                'Skip counting',
                'Pattern recognition',
            ],
        },
        {
            'subject': 'Mathematics',
            'topic': 'Fractions',
            'skills_practiced': ['Fraction operations', 'Simplifying fractions', 'Comparing fractions'],
            'main_subjects_covered': [
                'Adding fractions',
                'Subtracting fractions',
                'Equivalent fractions',
                'Mixed numbers',
            ],
        },
        {
            'subject': 'Mathematics',
            'topic': 'Decimals and Percentages',
            'skills_practiced': ['Decimal operations', 'Converting percentages', 'Place value'],
            'main_subjects_covered': ['Decimal notation', 'Percentage calculations', 'Money problems', 'Rounding'],
        },
        {
            'subject': 'Reading',
            'topic': 'Reading Comprehension',
            'skills_practiced': ['Reading fluency', 'Text analysis', 'Vocabulary building'],
            'main_subjects_covered': [
                'Main idea identification',
                'Context clues',
                'Character analysis',
                'Story elements',
            ],
        },
    ],
    '8th Grade': [
        {
            'subject': 'Mathematics',
            'topic': 'Linear Functions',
            'skills_practiced': ['Graphing', 'Slope calculation', 'Y-intercept'],
            'main_subjects_covered': [
                'Slope-intercept form',
                'Point-slope form',
                'Graphing linear equations',
                'Finding intercepts',
            ],
        },
        {
            'subject': 'Mathematics',
            'topic': 'Quadratic Equations',
            'skills_practiced': ['Completing the square', 'Factoring', 'Problem solving'],
            'main_subjects_covered': [
                'Quadratic formula',
                'Completing the square',
                'Word problems',
                'Graphing parabolas',
            ],
        },
        {
            'subject': 'Mathematics',
            'topic': 'Systems of Equations',
            'skills_practiced': ['Substitution method', 'Elimination method', 'Graphing systems'],
            'main_subjects_covered': ['Solving systems', 'Applications', 'Linear inequalities', 'Word problems'],
        },
        {
            'subject': 'Science',
            'topic': 'Chemistry Basics',
            'skills_practiced': ['Chemical formulas', 'Balancing equations', 'Lab techniques'],
            'main_subjects_covered': ['Atomic structure', 'Periodic table', 'Chemical reactions', 'States of matter'],
        },
    ],
    '10th Grade': [
        {
            'subject': 'Mathematics',
            'topic': 'Derivatives',
            'skills_practiced': ['Power rule', 'Chain rule', 'Differentiation'],
            'main_subjects_covered': [
                'Power rule for differentiation',
                'Chain rule introduction',
                'Basic derivative rules',
                'Applications of derivatives',
            ],
        },
        {
            'subject': 'Mathematics',
            'topic': 'Trigonometry',
            'skills_practiced': ['Sin/cos/tan functions', 'Unit circle', 'Trigonometric identities'],
            'main_subjects_covered': [
                'Trigonometric ratios',
                'Graphing trig functions',
                'Solving triangles',
                'Applications',
            ],
        },
        {
            'subject': 'Mathematics',
            'topic': 'Logarithms',
            'skills_practiced': ['Log properties', 'Exponential functions', 'Solving equations'],
            'main_subjects_covered': [
                'Properties of logarithms',
                'Change of base',
                'Exponential growth',
                'Applications',
            ],
        },
        {
            'subject': 'Physics',
            'topic': 'Kinematics',
            'skills_practiced': ['Motion calculations', 'Graphing motion', 'Problem solving'],
            'main_subjects_covered': ['Velocity and acceleration', 'Motion graphs', 'Free fall', 'Projectile motion'],
        },
    ],
}

# Common time slots
time_slots = ['9:00 AM', '10:30 AM', '2:00 PM', '3:00 PM', '4:30 PM', '6:00 PM']

# Sample notes patterns
notes_patterns = [
    '{student} showed good progress with {topic}. {improvement_area}',
    'Great session working on {topic}. {student} {positive_observation}. {area_to_focus}',
    '{student} {struggled_or_excelled} with {topic}. {future_focus}',
    'Productive lesson on {topic}. {student} demonstrated {strength}. {next_steps}',
]


def generate_lessons_for_student(student_id: int, student_name: str, grade: str, num_lessons: int = 8) -> list:
    """Generate lessons for a student with recent and future dates"""
    lessons = []
    templates = lesson_templates.get(grade, lesson_templates['8th Grade'])

    # Generate dates: 60% past (last 4 weeks), 40% future (next 3 weeks)
    past_lessons = int(num_lessons * 0.6)
    future_lessons = num_lessons - past_lessons

    today = datetime.now().date()

    # Past lessons (last 4 weeks)
    past_dates = []
    for i in range(past_lessons):
        days_ago = random.randint(1, 28)  # 1-28 days ago
        lesson_date = today - timedelta(days=days_ago)
        past_dates.append(lesson_date)

    # Future lessons (next 3 weeks)
    future_dates = []
    for i in range(future_lessons):
        days_ahead = random.randint(1, 21)  # 1-21 days ahead
        lesson_date = today + timedelta(days=days_ahead)
        future_dates.append(lesson_date)

    all_dates = sorted(past_dates + future_dates)

    for i, lesson_date in enumerate(all_dates):
        template = random.choice(templates)

        # Generate realistic notes
        notes_template = random.choice(notes_patterns)
        improvement_areas = [
            'Still needs practice with word problems.',
            'Could benefit from more practice with applications.',
            'Needs to work on speed and accuracy.',
            'Should focus on showing work clearly.',
        ]

        positive_observations = [
            'grasped the concepts quickly',
            'showed excellent problem-solving skills',
            'demonstrated strong understanding',
            'was very engaged and asked good questions',
        ]

        areas_to_focus = [
            'Continue practicing similar problems.',
            'Review fundamentals in next session.',
            'Focus on real-world applications next time.',
            'Work on building confidence with challenging problems.',
        ]

        notes = notes_template.format(
            student=student_name,
            topic=template['topic'].lower(),
            improvement_area=random.choice(improvement_areas),
            positive_observation=random.choice(positive_observations),
            area_to_focus=random.choice(areas_to_focus),
            struggled_or_excelled=random.choice(['struggled initially', 'excelled']),
            strength=random.choice(['good analytical thinking', 'strong foundational knowledge', 'persistence']),
            future_focus=random.choice(improvement_areas),
            next_steps=random.choice(areas_to_focus),
        )

        # Generate strengths and weaknesses observed
        general_strengths = [
            'Quick to understand new concepts',
            'Good problem-solving approach',
            'Asks thoughtful questions',
            'Shows work clearly',
            'Good attention to detail',
            'Persistent when facing challenges',
        ]

        general_weaknesses = [
            'Sometimes rushes through problems',
            'Needs more practice with basics',
            'Could improve organization of work',
            'Needs confidence building',
            'Sometimes forgets to check answers',
        ]

        tutor_tips = [
            'Continue reinforcing fundamental concepts',
            'Use visual aids to support learning',
            'Encourage showing all work steps',
            'Practice timed exercises to build fluency',
            'Connect concepts to real-world examples',
            'Celebrate progress to build confidence',
        ]

        lesson = {
            'student_id': student_id,
            'date': lesson_date.strftime('%Y-%m-%d'),
            'start_time': random.choice(time_slots),
            'subject': template['subject'],
            'topic': template['topic'],
            'duration': random.choice([45, 60, 75, 90]),
            'notes': notes,
            'skills_practiced': template['skills_practiced'],
            'main_subjects_covered': template['main_subjects_covered'],
            'student_strengths_observed': random.sample(general_strengths, k=random.randint(2, 4)),
            'student_weaknesses_observed': random.sample(general_weaknesses, k=random.randint(1, 3)),
            'tutor_tips': random.sample(tutor_tips, k=random.randint(3, 5)),
        }

        lessons.append(lesson)

    return lessons


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

        print('Generating lessons with recent and future dates...')
        all_lessons = []

        # Generate 8 lessons per student (5 past, 3 future)
        for student in students:
            student_lessons = generate_lessons_for_student(
                student_id=student.id, student_name=student.name, grade=student.grade, num_lessons=8
            )
            all_lessons.extend(student_lessons)

        print(f'Seeding {len(all_lessons)} lessons...')
        for lesson_data in all_lessons:
            lesson = Lesson(**lesson_data)
            session.add(lesson)

        session.commit()

        print('Database seeded successfully!')
        print(f'Created {len(students_data)} students and {len(all_lessons)} lessons')

        # Show breakdown of past vs future lessons
        today = datetime.now().date()
        past_lessons = sum(1 for lesson in all_lessons if datetime.strptime(lesson['date'], '%Y-%m-%d').date() < today)
        future_lessons = len(all_lessons) - past_lessons
        print(f'  - {past_lessons} past lessons')
        print(f'  - {future_lessons} future lessons')


if __name__ == '__main__':
    seed_database()
