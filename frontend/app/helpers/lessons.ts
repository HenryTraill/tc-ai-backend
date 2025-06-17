import type { Student } from "~/data/api";
import { fullName } from "./students";

export const formatStudentNames = (students: Student[]): string => {
  if (!students || students.length === 0) return 'Unknown Students';

  const firstStudentName = fullName(students[0]);

  if (students.length === 1) return firstStudentName;

  return `${firstStudentName} + ${students.length - 1}`;
};


export function getDurationBetween(start: string, end: string): string {
  const startDate = new Date(start);
  const endDate = new Date(end);

  const diffMs = endDate.getTime() - startDate.getTime();
  if (isNaN(diffMs) || diffMs < 0) return "Invalid duration";

  const totalMinutes = Math.floor(diffMs / (1000 * 60));
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;

  const parts = [];
  if (hours > 0) parts.push(`${hours} hour${hours > 1 ? "s" : ""}`);
  if (minutes > 0) parts.push(`${minutes} minute${minutes > 1 ? "s" : ""}`);

  return parts.length > 0 ? parts.join(" ") : "0 minutes";
}

export const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-GB', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    timeZone: 'Europe/London',
  });
};

export function formatTime(timestamp: string): string {
  const date = new Date(timestamp + 'Z');
  return date.toLocaleTimeString('en-GB', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
    timeZone: 'Europe/London',
  });
}

export function formatTimeForInput(timestamp: string): string {
  const date = new Date(timestamp + 'Z'); // treat as UTC
  return date.toLocaleTimeString('en-GB', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    timeZone: 'Europe/London',
  });
}

export function getReadableLessonStatus(status: string): string {
  switch (status) {
    case 'planned':
      return 'Planned';
    case 'pending':
      return 'Pending';
    case 'complete':
      return 'Complete';
    case 'cancelled':
      return 'Cancelled';
    case 'cancelled-but-chargeable':
      return 'Cancelled (Chargeable)';
    default:
      return 'Unknown';
  }
}