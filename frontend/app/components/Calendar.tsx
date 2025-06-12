import { useState } from 'react';
import { Link } from 'react-router';
import type { Lesson } from '~/data/api';
import { formatTime } from '~/helpers/lessons';
import { Button } from './ui/Button';

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
    small: 'text-xs p-1 sm:p-2',
    medium: 'text-sm p-2 sm:p-3',
    large: 'text-base p-3 sm:p-4'
  };

  return (
    <Link to={`/lessons/${lesson.id}`}
      className={`${sizeClasses[size]} rounded border bg-cream cursor-pointer hover:opacity-50 transition-opacity flex flex-col text-navy-blue min-h-[60px] sm:min-h-auto`}
    >
      <p className="font-medium truncate sm:whitespace-normal" title={lesson.topic}>
        {lesson.topic}
      </p>

      <div className="flex items-center gap-1 mt-1 text-xs">
        <i className="fas fa-user flex-shrink-0"></i>
        <span className="truncate" title={lesson.studentName}>{lesson.studentName}</span>
      </div>

      <div className="flex items-center gap-1 mt-1 text-xs">
        <i className="fas fa-clock flex-shrink-0"></i>
        <span>{formatTime(lesson.start_dt)}</span>
      </div>
    </Link>
  );
};

// Mobile-first list view for small screens
const MobileListView = ({ currentDate, lessons }: { currentDate: Date, lessons: Lesson[] }) => {
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
    <div className="bg-white rounded-xl shadow-sm border w-full">
      {days.map((day, index) => {
        const dayLessons = lessonUtils.sortLessonsByTime(lessonUtils.getLessonsForDay(lessons, day));
        const isToday = dateUtils.isSameDay(day, today);

        return (
          <div
            key={index}
            className={`p-4 border-b last:border-b-0 ${isToday ? 'bg-baby-blue' : ''}`}
          >
            <div className="flex items-center justify-between mb-3">
              <h3 className={`font-semibold text-lg ${isToday ? 'text-dark-blue' : 'text-navy-blue'}`}>
                {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][index]} {dateUtils.format(day, 'd')}
              </h3>
              <span className="text-sm text-gray-500">
                {dayLessons.length} lesson{dayLessons.length !== 1 ? 's' : ''}
              </span>
            </div>

            <div className="space-y-2">
              {dayLessons.length > 0 ? (
                dayLessons.map(lesson => (
                  <LessonCard key={lesson.id} lesson={lesson} size="medium" showDate={false} />
                ))
              ) : (
                <div className="text-sm text-gray-400 italic py-2">No lessons</div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};

const MonthView = ({ currentDate, lessons, onDateSelect, onViewChange }: {
  currentDate: Date,
  lessons: Lesson[],
  onDateSelect: (date: Date) => void,
  onViewChange: (view: 'month' | 'week' | 'day') => void
}) => {
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
    <div className="bg-white rounded-xl shadow-sm border w-full">
      <div className="overflow-hidden bg-light-blue rounded-t-xl sticky top-0 z-10 grid grid-cols-7 border-b border-navy-blue">
        {['S', 'M', 'T', 'W', 'T', 'F', 'S'].map((day, index) => (
          <div
            key={index}
            className="p-2 sm:p-4 text-center font-semibold text-navy-blue text-xs sm:text-base"
          >
            <span className="sm:hidden">{day}</span>
            <span className="hidden sm:inline">
              {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][index]}
            </span>
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
              className={`min-h-16 sm:min-h-32 p-1 sm:p-2 border-r border-b relative ${!isCurrentMonth ? 'opacity-40' : ''}`}
              style={{
                borderColor: 'var(--color-baby-blue)',
                backgroundColor: isToday ? 'var(--color-baby-blue)' : 'white'
              }}
            >
              <div className={`text-xs sm:text-sm font-medium mb-1 sm:mb-2 ${isToday ? 'font-bold' : ''}`}
                style={{
                  color: isToday ? 'var(--color-dark-blue)' : isCurrentMonth ? 'var(--color-navy-blue)' : 'var(--color-navy-blue-50)'
                }}>
                {dateUtils.format(day, 'd')}
              </div>

              {/* Show lesson count on mobile, actual lessons on desktop */}
              <div className="sm:hidden">
                {dayLessons.length > 0 && (
                  <button
                    onClick={() => {
                      onDateSelect(day);
                      onViewChange('day');
                    }}
                    className="text-xs rounded px-1 py-0.5 text-center w-full hover:opacity-80 transition-opacity"
                    style={{
                      backgroundColor: 'var(--color-navy-blue)',
                      color: 'white'
                    }}
                  >
                    {dayLessons.length} lesson{dayLessons.length !== 1 ? 's' : ''}
                  </button>
                )}
              </div>

              <div className="hidden sm:block space-y-1">
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
                    +{dayLessons.length - 2}
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
    <>
      {/* Mobile view: List format */}
      <div className="lg:hidden">
        <MobileListView currentDate={currentDate} lessons={lessons} />
      </div>

      {/* Desktop view: Grid format */}
      <div className="hidden lg:block bg-white rounded-xl shadow-sm overflow-hidden border w-full">
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
    </>
  );
};

const DayView = ({ currentDate, lessons }: { currentDate: Date, lessons: Lesson[] }) => {
  const dayLessons = lessonUtils.sortLessonsByTime(lessonUtils.getLessonsForDay(lessons, currentDate));
  const today = new Date();
  const isToday = dateUtils.isSameDay(currentDate, today);

  return (
    <div className="bg-white rounded-xl shadow-sm overflow-hidden border w-full">
      <div
        className="p-4 sm:p-6 text-center border-b"
        style={{
          backgroundColor: isToday ? 'var(--color-baby-blue)' : 'var(--color-light-blue)',
          borderColor: 'var(--color-baby-blue)',
          color: 'var(--color-navy-blue)'
        }}
      >
        <h2 className="text-xl sm:text-2xl font-bold">
          {dateUtils.format(currentDate, 'dddd, MMMM d')}
        </h2>
        <p className="text-sm opacity-75 mt-1">
          {dayLessons.length} lesson{dayLessons.length !== 1 ? 's' : ''} scheduled
        </p>
      </div>

      <div className="p-4 sm:p-6">
        {dayLessons.length > 0 ? (
          <div className="space-y-3 sm:space-y-4">
            {dayLessons.map(lesson => (
              <LessonCard key={lesson.id} lesson={lesson} size="large" showDate={false} />
            ))}
          </div>
        ) : (
          <div className="text-center py-8 sm:py-12">
            <i className="fas fa-calendar-times text-3xl sm:text-4xl text-gray-300 mb-4"></i>
            <p className="text-gray-500">No lessons scheduled for this day</p>
          </div>
        )}
      </div>
    </div>
  );
};

const Calendar = ({ lessons }: { lessons: Lesson[] }) => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [view, setView] = useState<'month' | 'week' | 'day'>('month');

  const today = new Date();

  const getNavigationLabel = () => {
    switch (view) {
      case 'day':
        return dateUtils.format(currentDate, 'MMMM d, yyyy');
      case 'week': {
        const weekStart = dateUtils.startOfWeek(new Date(currentDate));
        const weekEnd = dateUtils.addDays(weekStart, 6);
        return `${dateUtils.format(weekStart, 'MMM d')} - ${dateUtils.format(weekEnd, 'MMM d, yyyy')}`;
      }
      case 'month':
      default:
        return dateUtils.format(currentDate, 'MMMM yyyy');
    }
  };

  const isTodayView = () => {
    switch (view) {
      case 'day':
        return dateUtils.isSameDay(currentDate, today);
      case 'week': {
        const start = dateUtils.startOfWeek(currentDate);
        const end = dateUtils.addDays(start, 6);
        return today >= start && today <= end;
      }
      case 'month':
        return currentDate.getMonth() === today.getMonth() && currentDate.getFullYear() === today.getFullYear();
      default:
        return false;
    }
  };

  const handleTodayClick = () => {
    setCurrentDate(new Date());
  };

  const navigate = (direction: 'next' | 'prev') => {
    const newDate = new Date(currentDate);
    switch (view) {
      case 'day':
        setCurrentDate(dateUtils.addDays(newDate, direction === 'next' ? 1 : -1));
        break;
      case 'week':
        setCurrentDate(dateUtils.addWeeks(newDate, direction === 'next' ? 1 : -1));
        break;
      case 'month':
        newDate.setMonth(newDate.getMonth() + (direction === 'next' ? 1 : -1));
        setCurrentDate(newDate);
        break;
    }
  };

  const renderView = () => {
    switch (view) {
      case 'day':
        return <DayView currentDate={currentDate} lessons={lessons} />;
      case 'week':
        return <WeekView currentDate={currentDate} lessons={lessons} />;
      case 'month':
      default:
        return <MonthView currentDate={currentDate} lessons={lessons} onDateSelect={setCurrentDate} onViewChange={setView} />;
    }
  };

  return (
    <div className="px-2 sm:px-0">
      {/* Mobile-first header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 sm:mb-8 gap-4">
        <h1 className="text-2xl sm:text-4xl font-bold text-slate-800">Calendar</h1>

        {/* Mobile controls stack vertically */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 sm:gap-4">
          {/* View selector */}
          <div className="min-w-22 relative">
            <select
              value={view}
              onChange={(e) => setView(e.target.value as 'month' | 'week' | 'day')}
              className="w-full sm:w-auto appearance-none bg-white border border-gray-300 rounded-lg px-4 py-2 pr-8 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
              style={{ color: 'var(--color-navy-blue)' }}
            >
              <option value="month">Month</option>
              <option value="week">Week</option>
              <option value="day">Day</option>
            </select>
            <i className="fas fa-fw fa-chevron-down absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 text-xs pointer-events-none"></i>
          </div>

          <div className="flex items-center justify-between sm:justify-start gap-2 sm:gap-4">
            <Button
              onClick={handleTodayClick}
              disabled={isTodayView()}
            >
              Today
            </Button>

            <div className="flex items-center gap-1 sm:gap-0">
              <button
                onClick={() => navigate('prev')}
                className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                aria-label="Previous"
              >
                <i className="fas fa-fw fa-chevron-left text-lg"></i>
              </button>

              <h3 className="text-base sm:text-xl font-semibold text-center text-navy-blue px-2 sm:px-4 min-w-0">
                {getNavigationLabel()}
              </h3>

              <button
                onClick={() => navigate('next')}
                className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                aria-label="Next"
              >
                <i className="fas fa-fw fa-chevron-right text-lg"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      {renderView()}
    </div>
  );
};

export default Calendar;