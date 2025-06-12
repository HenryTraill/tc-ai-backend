import { useState } from 'react';
import { Link } from 'react-router';
import type { Lesson } from '~/data/api';
import { formatTime } from '~/helpers/lessons';

const dateUtils = {
  startOfMonth: (date: Date) => {
    return new Date(date.getFullYear(), date.getMonth(), 1);
  },

  endOfMonth: (date: Date) => {
    return new Date(date.getFullYear(), date.getMonth() + 1, 0);
  },

  startOfWeek: (date: Date) => {
    const day = date.getDay();
    const diff = date.getDate() - day;
    return new Date(date.setDate(diff));
  },

  startOfDay: (date: Date) => {
    return new Date(date.getFullYear(), date.getMonth(), date.getDate());
  },

  addDays: (date: Date, days: number) => {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
  },

  addWeeks: (date: Date, weeks: number) => {
    return dateUtils.addDays(date, weeks * 7);
  },

  isSameDay: (date1: Date, date2: Date) => {
    return date1.getDate() === date2.getDate() &&
      date1.getMonth() === date2.getMonth() &&
      date1.getFullYear() === date2.getFullYear();
  },

  format: (date: Date, formatStr: string) => {
    const months = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];

    const days = [
      'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'
    ];

    if (formatStr === 'MMMM yyyy') {
      return `${months[date.getMonth()]} ${date.getFullYear()}`;
    }
    if (formatStr === 'MMMM d, yyyy') {
      return `${months[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;
    }
    if (formatStr === 'dddd, MMMM d') {
      return `${days[date.getDay()]}, ${months[date.getMonth()]} ${date.getDate()}`;
    }
    if (formatStr === 'MMM d') {
      return `${months[date.getMonth()].substring(0, 3)} ${date.getDate()}`;
    }
    return date.getDate().toString();
  }
};

const lessonUtils = {
  getLessonsForDay: (lessons: Lesson[], date: Date) => {
    return lessons.filter(lesson => dateUtils.isSameDay(new Date(lesson.start_dt), date));
  },

  getTypeColor: (type: any) => {
    const colors = {
      piano: 'bg-blue-100 text-blue-800 border-blue-200',
      guitar: 'bg-green-100 text-green-800 border-green-200',
      voice: 'bg-purple-100 text-purple-800 border-purple-200',
      drums: 'bg-orange-100 text-orange-800 border-orange-200'
    };
    return colors[type] || 'bg-gray-100 text-gray-800 border-gray-200';
  },

  sortLessonsByTime: (lessons: Lesson[]) => {
    return lessons.sort((a, b) => {
      const timeA = new Date(`1970/01/01 ${a.start_dt}`);
      const timeB = new Date(`1970/01/01 ${b.start_dt}`);
      return Number(timeA) - Number(timeB);
    });
  }
};

const LessonCard = ({ lesson, size = 'small', showDate = false }: { lesson: Lesson, size: string, showDate: boolean }) => {
  const sizeClasses = {
    small: 'text-xs p-1',
    medium: 'text-sm p-2',
    large: 'text-base p-3'
  };

  return (
    <Link to={`/lessons/${lesson.id}`}
      className={`${sizeClasses[size]} rounded border bg-cream cursor-pointer hover:opacity-50 transition-opacity flex flex-col text-navy-blue`}
    >
      <p className="font-medium">{lesson.topic}</p>

      <div className="flex items-center gap-1 mt-1 text-xs">
        <i className="fas fa-user"></i>
        <span>{lesson.studentName}</span>
      </div>

      <div className="flex items-center gap-1 mt-1 text-xs">
        <i className="fas fa-clock"></i>
        <span>{formatTime(lesson.start_dt)}</span>
      </div>
    </Link>
  );
};

const MonthView = ({ currentDate, lessons }: { currentDate: Date, lessons: Lesson[] }) => {
  const getDaysInMonth = () => {
    const start = dateUtils.startOfMonth(currentDate);
    const startDate = dateUtils.startOfWeek(new Date(start));

    const days = [];
    let day = new Date(startDate);

    for (let i = 0; i < 42; i++) {
      days.push(new Date(day));
      day = dateUtils.addDays(day, 1);
    }

    return days;
  };

  const days = getDaysInMonth();
  const today = new Date();

  return (
    <div className="bg-white rounded-xl shadow-sm overflow-hidden border w-full">
      <div className="grid grid-cols-7 border-b" style={{ borderColor: 'var(--color-baby-blue)' }}>
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
          <div
            key={day}
            className="p-4 text-center font-semibold"
            style={{ backgroundColor: 'var(--color-light-blue)', color: 'var(--color-navy-blue)' }}
          >
            {day}
          </div>
        ))}
      </div>

      <div className="grid grid-cols-7">
        {days.map((day, index) => {
          const dayLessons = lessonUtils.getLessonsForDay(lessons, day);
          const isCurrentMonth = day.getMonth() === currentDate.getMonth();
          const isToday = dateUtils.isSameDay(day, today);

          return (
            <div
              key={index}
              className={`min-h-32 p-2 border-r border-b relative ${!isCurrentMonth ? 'opacity-40' : ''}`}
              style={{
                borderColor: 'var(--color-baby-blue)',
                backgroundColor: isToday ? 'var(--color-baby-blue)' : 'white'
              }}
            >
              <div className={`text-sm font-medium mb-2 ${isToday ? 'font-bold' : ''}`}
                style={{
                  color: isToday ? 'var(--color-dark-blue)' : isCurrentMonth ? 'var(--color-navy-blue)' : 'var(--color-navy-blue-50)'
                }}>
                {dateUtils.format(day, 'd')}
              </div>

              <div className="space-y-1">
                {dayLessons.slice(0, 2).map(lesson => (
                  <LessonCard key={lesson.id} lesson={lesson} size="small" showDate={false} />
                ))}

                {dayLessons.length > 2 && (
                  <div
                    className="text-xs text-center py-1 rounded"
                    style={{
                      backgroundColor: 'var(--color-navy-blue-15)',
                      color: 'var(--color-navy-blue)'
                    }}
                  >
                    +{dayLessons.length - 2} more
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

const WeekView = ({ currentDate, lessons }: { currentDate: Date, lessons: Lesson[] }) => {
  const getWeekDays = () => {
    const startOfWeek = dateUtils.startOfWeek(new Date(currentDate));
    const days = [];
    for (let i = 0; i < 7; i++) {
      days.push(dateUtils.addDays(startOfWeek, i));
    }
    return days;
  };

  const days = getWeekDays();
  const today = new Date();

  return (
    <div className="bg-white rounded-xl shadow-sm overflow-hidden border w-full">
      <div className="grid grid-cols-7 border-b" style={{ borderColor: 'var(--color-baby-blue)' }}>
        {days.map((day, index) => {
          const isToday = dateUtils.isSameDay(day, today);
          return (
            <div
              key={index}
              className="p-4 text-center font-semibold"
              style={{
                backgroundColor: isToday ? 'var(--color-baby-blue)' : 'var(--color-light-blue)',
                color: 'var(--color-navy-blue)'
              }}
            >
              <div className="text-sm">{['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][index]}</div>
              <div className={`text-lg ${isToday ? 'font-bold' : ''}`}>
                {dateUtils.format(day, 'd')}
              </div>
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-7 min-h-96">
        {days.map((day, index) => {
          const dayLessons = lessonUtils.sortLessonsByTime(lessonUtils.getLessonsForDay(lessons, day));
          const isToday = dateUtils.isSameDay(day, today);

          return (
            <div
              key={index}
              className="p-3 border-r border-b"
              style={{
                borderColor: 'var(--color-baby-blue)',
                backgroundColor: isToday ? 'var(--color-baby-blue)' : 'white'
              }}
            >
              <div className="space-y-2">
                {dayLessons.map(lesson => (
                  <LessonCard key={lesson.id} lesson={lesson} size="medium" showDate={false} />
                ))}
                {dayLessons.length === 0 && (
                  <div className="text-xs text-gray-400 italic">No lessons</div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

const DayView = ({ currentDate, lessons }: { currentDate: Date, lessons: Lesson[] }) => {
  const dayLessons = lessonUtils.sortLessonsByTime(lessonUtils.getLessonsForDay(lessons, currentDate));
  const today = new Date();
  const isToday = dateUtils.isSameDay(currentDate, today);

  return (
    <div className="bg-white rounded-xl shadow-sm overflow-hidden border w-full">
      <div
        className="p-6 text-center border-b"
        style={{
          backgroundColor: isToday ? 'var(--color-baby-blue)' : 'var(--color-light-blue)',
          borderColor: 'var(--color-baby-blue)',
          color: 'var(--color-navy-blue)'
        }}
      >
        <h2 className="text-2xl font-bold">
          {dateUtils.format(currentDate, 'dddd, MMMM d')}
        </h2>
        <p className="text-sm opacity-75 mt-1">
          {dayLessons.length} lesson{dayLessons.length !== 1 ? 's' : ''} scheduled
        </p>
      </div>

      <div className="p-6">
        {dayLessons.length > 0 ? (
          <div className="space-y-4">
            {dayLessons.map(lesson => (
              <LessonCard key={lesson.id} lesson={lesson} size="large" showDate={false} />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <i className="fas fa-calendar-times text-4xl text-gray-300 mb-4"></i>
            <p className="text-gray-500">No lessons scheduled for this day</p>
          </div>
        )}
      </div>
    </div>
  );
};

const Calendar = ({ lessons }: { lessons: Lesson[] }) => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [view, setView] = useState('month');

  const getNavigationLabel = () => {
    switch (view) {
      case 'day':
        return dateUtils.format(currentDate, 'MMMM d, yyyy');
      case 'week':
        const weekStart = dateUtils.startOfWeek(new Date(currentDate));
        const weekEnd = dateUtils.addDays(weekStart, 6);
        return `${dateUtils.format(weekStart, 'MMM d')} - ${dateUtils.format(weekEnd, 'MMM d, yyyy')}`;
      case 'month':
      default:
        return dateUtils.format(currentDate, 'MMMM yyyy');
    }
  };

  const navigate = (direction: string) => {
    const newDate = new Date(currentDate);

    switch (view) {
      case 'day':
        setCurrentDate(dateUtils.addDays(newDate, direction === 'next' ? 1 : -1));
        break;
      case 'week':
        setCurrentDate(dateUtils.addWeeks(newDate, direction === 'next' ? 1 : -1));
        break;
      case 'month':
      default:
        newDate.setMonth(newDate.getMonth() + (direction === 'next' ? 1 : -1));
        setCurrentDate(newDate);
        break;
    }
  };

  const renderView = (lessons: Lesson[]) => {
    switch (view) {
      case 'day':
        return <DayView currentDate={currentDate} lessons={lessons} />;
      case 'week':
        return <WeekView currentDate={currentDate} lessons={lessons} />;
      case 'month':
      default:
        return <MonthView currentDate={currentDate} lessons={lessons} />;
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div className='flex items-center justify-between w-full'>
          <h1 className="text-4xl font-bold text-slate-800 flex-1">Calendar</h1>

          <div className="flex items-center gap-4">
            <div className="relative">
              <select
                value={view}
                onChange={(e) => setView(e.target.value)}
                className="appearance-none bg-white border border-gray-300 rounded-lg px-4 py-2 pr-8 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
                style={{ color: 'var(--color-navy-blue)' }}
              >
                <option value="month">Month</option>
                <option value="week">Week</option>
                <option value="day">Day</option>
              </select>
              <i className="fas fa-fw fa-chevron-down absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 text-xs pointer-events-none"></i>
            </div>

            <div className="flex items-center">
              <button
                onClick={() => navigate('prev')}
                className="p-2 rounded-lg hover:bg-opacity-80 transition-colors"
              >
                <i className="fas fa-fw fa-fw fa-chevron-left text-lg"></i>
              </button>
              <h3 className="text-xl font-semibold min-w-48 text-center text-navy-blue">
                {getNavigationLabel()}
              </h3>
              <button
                onClick={() => navigate('next')}
                className="p-2 rounded-lg hover:bg-opacity-80 transition-colors"
              >
                <i className="fas fa-fw fa-chevron-right text-lg"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      {renderView(lessons)}
    </div>
  );
};

export default Calendar;