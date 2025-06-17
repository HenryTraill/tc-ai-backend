#!/usr/bin/env python3
"""Seed the database with sample data"""

import random
from datetime import datetime, timedelta

from sqlmodel import Session, select

from app.core.auth import get_password_hash
from app.core.database import create_db_and_tables, engine
from app.models import Client, Company, Lesson, LessonStudent, LessonTutor, Student, TutorStudent, User, UserType

# Sample clients data
clients_data = [
    {
        'first_name': 'John',
        'last_name': 'Johnson',
        'email': 'johnson.family@example.com',
        'phone': '+1-555-0101',
        'address': '123 Oak Street, Springfield, IL',
        'notes': 'Parent prefers evening communication',
    },
    {
        'first_name': 'Li',
        'last_name': 'Chen',
        'email': 'chen.family@example.com',
        'phone': '+1-555-0102',
        'address': '456 Maple Avenue, Springfield, IL',
        'notes': 'Student is very motivated, parent involved',
    },
    {
        'first_name': 'Maria',
        'last_name': 'Rodriguez',
        'email': 'rodriguez.family@example.com',
        'phone': '+1-555-0103',
        'address': '789 Pine Road, Springfield, IL',
        'notes': 'Younger student, needs patient approach',
    },
]

# Sample students data (will be linked to clients)
students_data = [
    {
        'first_name': 'Emma',
        'last_name': 'Johnson',
        'email': 'emma.johnson@example.com',
        'phone': '+1-555-0111',
        'grade': '8th Grade',
        'strengths': ['Quick learner', 'Strong in algebra', 'Good problem-solving skills'],
        'weaknesses': ['Struggles with geometry', 'Needs work on word problems'],
    },
    {
        'first_name': 'Marcus',
        'last_name': 'Chen',
        'email': 'marcus.chen@example.com',
        'phone': '+1-555-0112',
        'grade': '10th Grade',
        'strengths': ['Excellent at calculus', 'Great attention to detail', 'Motivated student'],
        'weaknesses': ['Sometimes rushes through problems', 'Needs confidence building'],
    },
    {
        'first_name': 'Sofia',
        'last_name': 'Rodriguez',
        'email': 'sofia.rodriguez@example.com',
        'phone': '+1-555-0113',
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

        # Generate start and end datetime objects
        start_time_str = random.choice(time_slots)
        duration_minutes = random.choice([45, 60, 75, 90])

        # Parse the time string and create datetime objects
        if 'AM' in start_time_str or 'PM' in start_time_str:
            # Convert 12-hour format to 24-hour format
            time_part = start_time_str.replace(' AM', '').replace(' PM', '')
            hour, minute = map(int, time_part.split(':'))
            if 'PM' in start_time_str and hour != 12:
                hour += 12
            elif 'AM' in start_time_str and hour == 12:
                hour = 0
        else:
            # Assume 24-hour format
            hour, minute = map(int, start_time_str.split(':'))

        # Create start_dt and end_dt
        start_dt = datetime.combine(lesson_date, datetime.min.time().replace(hour=hour, minute=minute))
        end_dt = start_dt + timedelta(minutes=duration_minutes)

        lesson = {
            'start_dt': start_dt,
            'end_dt': end_dt,
            'subject': template['subject'],
            'topic': template['topic'],
            'notes': notes,
            'skills_practiced': template['skills_practiced'],
            'main_subjects_covered': template['main_subjects_covered'],
            'student_strengths_observed': random.sample(general_strengths, k=random.randint(2, 4)),
            'student_weaknesses_observed': random.sample(general_weaknesses, k=random.randint(1, 3)),
            'tutor_tips': random.sample(tutor_tips, k=random.randint(3, 5)),
            '_student_id': student_id,  # Store student_id separately for junction table creation
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

        print('Creating test company...')
        test_company = Company(
            name='Test Company',
            tc_id='123',
            tutorcruncher_domain='https://test.tutorcruncher.com',
        )
        session.add(test_company)
        session.commit()
        session.refresh(test_company)
        print(f'Created test company with ID: {test_company.id}')

        print('Creating test tutor user...')
        test_tutor = User(
            email='testing@tutorcruncher.com',
            hashed_password=get_password_hash('testing'),
            user_type=UserType.TUTOR,
            is_active=True,
            first_name='Test',
            last_name='Tutor',
        )
        session.add(test_tutor)
        session.commit()
        session.refresh(test_tutor)
        print(f'Created test tutor user with ID: {test_tutor.id}')

        print('Creating test admin user...')
        test_admin = User(
            email='admin@tutorcruncher.com',
            hashed_password=get_password_hash('testing'),
            user_type=UserType.ADMIN,
            is_active=True,
            first_name='Test',
            last_name='Admin',
            company_ids=[test_company.id],
        )
        session.add(test_admin)
        session.commit()
        session.refresh(test_admin)
        print(f'Created test admin user with ID: {test_admin.id}')

        print('Seeding clients...')
        clients = []
        for client_data in clients_data:
            client = Client(**client_data)
            session.add(client)
            clients.append(client)

        session.commit()

        # Refresh to get IDs
        for client in clients:
            session.refresh(client)

        print('Seeding students...')
        students = []
        for i, student_data in enumerate(students_data):
            # Link each student to the corresponding client
            student_data_with_client = student_data.copy()
            student_data_with_client['client_id'] = clients[i].id
            # Link student to company
            student_data_with_client['company_id'] = test_company.id

            student = Student(**student_data_with_client)
            session.add(student)
            students.append(student)

        session.commit()

        # Refresh to get IDs
        for student in students:
            session.refresh(student)
            # Create TutorStudent association
            tutor_student = TutorStudent(tutor_id=test_tutor.id, student_id=student.id)
            session.add(tutor_student)

        session.commit()

        print('Generating lessons with recent and future dates...')
        all_lessons = []

        # Generate 8 lessons per student (5 past, 3 future)
        for student in students:
            student_name = f'{student.first_name} {student.last_name}'
            student_lessons = generate_lessons_for_student(
                student_id=student.id, student_name=student_name, grade=student.grade, num_lessons=8
            )
            all_lessons.extend(student_lessons)

        print(f'Seeding {len(all_lessons)} lessons...')
        lesson_student_pairs = []  # Store student_id for each lesson for junction table

        for lesson_data in all_lessons:
            # Extract student_id before creating lesson
            student_id = lesson_data.pop('_student_id')
            # Add tutor_id to lesson data
            lesson_data['tutor_id'] = test_tutor.id
            lesson = Lesson(**lesson_data)
            session.add(lesson)
            lesson_student_pairs.append((lesson, student_id))

        session.commit()

        # Refresh all lessons to get their IDs
        for lesson, _ in lesson_student_pairs:
            session.refresh(lesson)

        # Now create junction table entries
        print('Creating lesson-student associations...')
        for lesson, student_id in lesson_student_pairs:
            lesson_student = LessonStudent(lesson_id=lesson.id, student_id=student_id)
            session.add(lesson_student)
            # Create LessonTutor association
            lesson_tutor = LessonTutor(lesson_id=lesson.id, tutor_id=test_tutor.id)
            session.add(lesson_tutor)
            # Link lesson to company
            lesson.company_id = test_company.id
            session.add(lesson)

        session.commit()

        print('Database seeded successfully!')
        print(f'Created {len(clients_data)} clients, {len(students_data)} students and {len(all_lessons)} lessons')
        print(f'Created test tutor user: {test_tutor.email}')
        print(f'Created test admin user: {test_admin.email}')

        # Show breakdown of past vs future lessons
        now = datetime.now()
        past_lessons = sum(1 for lesson in all_lessons if lesson['start_dt'] < now)
        future_lessons = len(all_lessons) - past_lessons
        print(f'  - {past_lessons} past lessons')
        print(f'  - {future_lessons} future lessons')


if __name__ == '__main__':
    seed_database()
