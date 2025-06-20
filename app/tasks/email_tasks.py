import logging

from ..core.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task
def send_lesson_reminder(student_id: int, lesson_id: int, email: str):
    """Send a lesson reminder email to a student"""
    # This is a placeholder task for sending email reminders
    # In a real implementation, you would integrate with an email service
    logger.info(f'Sending lesson reminder to student {student_id} for lesson {lesson_id} at {email}')

    # Simulate email sending
    import time

    time.sleep(2)  # Simulate processing time

    logger.info(f'Lesson reminder sent successfully to {email}')
    return {'status': 'sent', 'student_id': student_id, 'lesson_id': lesson_id}
