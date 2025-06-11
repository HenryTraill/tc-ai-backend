import React, { useState } from 'react';

// Custom Tailwind configuration would normally be in tailwind.config.js
// For this demo, we'll use the closest available Tailwind classes

const Calendar = () => {
  const [currentDate, setCurrentDate] = useState(new Date());

  // Sample lesson data - replace with your actual lessons
  const lessons = [
    {
      id: 1,
      title: "Beginner Piano",
      time: "10:00 AM",
      duration: "1h",
      instructor: "Sarah M.",
      location: "Room A",
      date: new Date(2025, 5, 12), // June 12, 2025
      type: "piano"
    },
    {
      id: 2,
      title: "Guitar Basics",
      time: "2:00 PM",
      duration: "45min",
      instructor: "Mike R.",
      location: "Room B",
      date: new Date(2025, 5, 12),
      type: "guitar"
    },
    {
      id: 3,
      title: "Voice Training",
      time: "11:00 AM",
      duration: "30min",
      instructor: "Emma L.",
      location: "Studio 1",
      date: new Date(2025, 5, 15),
      type: "voice"
    },
    {
      id: 4,
      title: "Advanced Piano",
      time: "3:00 PM",
      duration: "1h 30min",
      instructor: "David K.",
      location: "Room A",
      date: new Date(2025, 5, 18),
      type: "piano"
    },
    {
      id: 5,
      title: "Drum Workshop",
      time: "4:00 PM",
      duration: "2h",
      instructor: "Alex J.",
      location: "Studio 2",
      date: new Date(2025, 5, 20),
      type: "drums"
    }
  ];

  const startOfMonth = (date) => {
    return new Date(date.getFullYear(), date.getMonth(), 1);
  };

  const endOfMonth = (date) => {
    return new Date(date.getFullYear(), date.getMonth() + 1, 0);
  };

  const startOfWeek = (date) => {
    const day = date.getDay();
    const diff = date.getDate() - day;
    return new Date(date.setDate(diff));
  };

  const addDays = (date, days) => {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
  };

  const isSameDay = (date1: Date, date2: Date) => {
    return date1.getDate() === date2.getDate() &&
      date1.getMonth() === date2.getMonth() &&
      date1.getFullYear() === date2.getFullYear();
  };

  const format = (date: Date, formatStr) => {
    const months = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];

    if (formatStr === 'MMMM yyyy') {
      return `${months[date.getMonth()]} ${date.getFullYear()}`;
    }
    return date.getDate().toString();
  };

  const previousMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1));
  };

  const nextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1));
  };

  const getDaysInMonth = () => {
    const start = startOfMonth(currentDate);
    const end = endOfMonth(currentDate);
    const startDate = startOfWeek(new Date(start));

    const days = [];
    let day = new Date(startDate);

    for (let i = 0; i < 42; i++) {
      days.push(new Date(day));
      day = addDays(day, 1);
    }

    return days;
  };

  const getLessonsForDay = (date: Date) => {
    return lessons.filter(lesson => isSameDay(lesson.date, date));
  };

  const getTypeColor = (type: string) => {
    const colors = {
      piano: 'bg-blue-100 text-blue-800 border-blue-200',
      guitar: 'bg-green-100 text-green-800 border-green-200',
      voice: 'bg-purple-100 text-purple-800 border-purple-200',
      drums: 'bg-orange-100 text-orange-800 border-orange-200'
    };
    return colors[type] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const days = getDaysInMonth();
  const today = new Date();

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div className='flex items-center justify-between w-full'>
          <h1 className="text-4xl font-bold text-slate-800 flex-1">Calendar</h1>
          <div className="flex items-center">
            <button
              onClick={previousMonth}
              className="p-2 rounded-lg hover:bg-opacity-80 transition-colors"
            >
              <i className="fas fa-chevron-left text-lg"></i>
            </button>
            <h3 className="text-xl font-semibold min-w-38 text-center text-navy-blue">
              {format(currentDate, 'MMMM yyyy')}
            </h3>
            <button
              onClick={nextMonth}
              className="p-2 rounded-lg hover:bg-opacity-80 transition-colors"
            >
              <i className="fas fa-chevron-right text-lg"></i>
            </button>
          </div>
        </div>
      </div>

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
            const dayLessons = getLessonsForDay(day);
            const isCurrentMonth = day.getMonth() === currentDate.getMonth();
            const isToday = isSameDay(day, today);

            return (
              <div
                key={index}
                className={`min-h-32 p-2 border-r border-b relative ${!isCurrentMonth ? 'opacity-40' : ''
                  }`}
                style={{
                  borderColor: 'var(--color-baby-blue)',
                  backgroundColor: isToday ? 'var(--color-baby-blue)' : 'white'
                }}
              >
                <div className={`text-sm font-medium mb-2 ${isToday ? 'font-bold' : ''
                  }`} style={{
                    color: isToday ? 'var(--color-dark-blue)' : isCurrentMonth ? 'var(--color-navy-blue)' : 'var(--color-navy-blue-50)'
                  }}>
                  {format(day, 'd')}
                </div>

                <div className="space-y-1">
                  {dayLessons.slice(0, 2).map(lesson => (
                    <div
                      key={lesson.id}
                      className={`text-xs p-1 rounded border ${getTypeColor(lesson.type)} cursor-pointer hover:opacity-80 transition-opacity`}
                      title={`${lesson.title} - ${lesson.time} with ${lesson.instructor}`}
                    >
                      <div className="font-medium truncate">{lesson.title}</div>
                      <div className="flex items-center gap-1 mt-1">
                        <i className="fas fa-clock text-xs"></i>
                        <span>{lesson.time}</span>
                      </div>
                    </div>
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

      <div className="mt-6 flex flex-wrap gap-4 justify-center">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded bg-blue-100 border border-blue-200"></div>
          <span className="text-sm">Piano</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded bg-green-100 border border-green-200"></div>
          <span className="text-sm">Guitar</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded bg-purple-100 border border-purple-200"></div>
          <span className="text-sm">Voice</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded bg-orange-100 border border-orange-200"></div>
          <span className="text-sm text-navy-blue">Drums</span>
        </div>
      </div>
    </div>
  );
};

export default Calendar;