from .client import Client, ClientCreate, ClientRead, ClientUpdate
from .company import Company, CompanyCreate, CompanyRead, CompanyUpdate
from .lesson import Lesson, LessonCreate, LessonRead, LessonStatus, LessonUpdate
from .lesson_student import LessonStudent
from .lesson_tutor import LessonTutor, LessonTutorCreate, LessonTutorRead
from .student import Student, StudentCreate, StudentRead, StudentUpdate
from .tutor_student import TutorStudent, TutorStudentCreate, TutorStudentRead
from .user import Token, TokenData, User, UserLogin, UserRead, UserType, UserUpdate

# Rebuild models to resolve forward references
LessonRead.model_rebuild()
StudentRead.model_rebuild()

__all__ = [
    'Client',
    'ClientCreate',
    'ClientUpdate',
    'ClientRead',
    'Company',
    'CompanyCreate',
    'CompanyUpdate',
    'CompanyRead',
    'Student',
    'StudentCreate',
    'StudentUpdate',
    'StudentRead',
    'Lesson',
    'LessonCreate',
    'LessonUpdate',
    'LessonRead',
    'LessonStatus',
    'LessonStudent',
    'User',
    'UserUpdate',
    'UserRead',
    'UserType',
    'UserLogin',
    'Token',
    'TokenData',
    'TutorStudent',
    'TutorStudentCreate',
    'TutorStudentRead',
    'LessonTutor',
    'LessonTutorCreate',
    'LessonTutorRead',
]
