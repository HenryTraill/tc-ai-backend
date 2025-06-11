import { useForm } from "react-hook-form";
import { useNavigate } from "react-router";
import { lessonsApi, type Student } from "../../data/api";
import { Button } from "../ui/Button";

// Define the shape of a lesson
interface LessonData {
  id?: number;
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
}

type LessonFormProps = {
  students: Student[];
  lesson?: LessonData;
};

export const LessonForm = ({ students, lesson }: LessonFormProps) => {
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    control,
    reset,
    formState: { isSubmitting }
  } = useForm({
    defaultValues: {
      student_id: lesson?.student_id?.toString() ?? '',
      date: lesson?.date ?? '',
      start_time: lesson?.start_time ?? '',
      subject: lesson?.subject ?? '',
      topic: lesson?.topic ?? '',
      duration: lesson?.duration ?? 60,
      notes: lesson?.notes ?? '',
      skills_practiced: lesson?.skills_practiced?.map(v => ({ value: v })) ?? [{ value: '' }],
      main_subjects_covered: lesson?.main_subjects_covered?.map(v => ({ value: v })) ?? [{ value: '' }],
      student_strengths_observed: lesson?.student_strengths_observed?.map(v => ({ value: v })) ?? [{ value: '' }],
      student_weaknesses_observed: lesson?.student_weaknesses_observed?.map(v => ({ value: v })) ?? [{ value: '' }],
      tutor_tips: lesson?.tutor_tips?.map(v => ({ value: v })) ?? [{ value: '' }]
    }
  });

  const onSubmit = async (data: any) => {
    const cleaned = {
      ...data,
      student_id: parseInt(data.student_id),
      duration: parseInt(data.duration),
      skills_practiced: data.skills_practiced.map(i => i.value).filter(Boolean),
      main_subjects_covered: data.main_subjects_covered.map(i => i.value).filter(Boolean),
      student_strengths_observed: data.student_strengths_observed.map(i => i.value).filter(Boolean),
      student_weaknesses_observed: data.student_weaknesses_observed.map(i => i.value).filter(Boolean),
      tutor_tips: data.tutor_tips.map(i => i.value).filter(Boolean)
    };

    const response = lesson
      ? await lessonsApi.update(lesson.id!, cleaned)
      : await lessonsApi.create(cleaned);

    if (response) {
      lesson ? navigate(`/lessons/${response.id}`) : navigate("/lessons");
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-8 min-h-full bg-cream">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="bg-white border shadow-sm p-6 rounded-xl">
          <h2 className="text-xl font-semibold text-slate-800 mb-4">Basic Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div>
              <label className="text-sm font-medium text-slate-700 mb-1 block">Student</label>
              <select {...register("student_id")} required className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2">
                <option value="">Select a student</option>
                {students.map((student) => (
                  <option key={student.id} value={student.id}>{student.name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-sm font-medium text-slate-700 mb-1 block">Date</label>
              <input type="date" {...register("date")} required className="w-full px-3 py-2 border rounded-lg focus:ring-2" />
            </div>

            <div>
              <label className="text-sm font-medium text-slate-700 mb-1 block">Start Time</label>
              <input type="string" {...register("start_time")} required className="w-full px-3 py-2 border rounded-lg focus:ring-2" />
            </div>

            <div>
              <label className="text-sm font-medium text-slate-700 mb-1 block">Subject</label>
              <input type="text" {...register("subject")} required className="w-full px-3 py-2 border rounded-lg focus:ring-2" />
            </div>

            <div>
              <label className="text-sm font-medium text-slate-700 mb-1 block">Topic</label>
              <input type="text" {...register("topic")} required className="w-full px-3 py-2 border rounded-lg focus:ring-2" />
            </div>

            <div>
              <label className="text-sm font-medium text-slate-700 mb-1 block">Duration</label>
              <input type="number" {...register("duration")} required min="1" className="w-full px-3 py-2 border rounded-lg focus:ring-2" />
            </div>
          </div>
        </div>

        <div className="bg-white border shadow-sm p-6 rounded-xl">
          <h2 className="text-xl font-semibold text-slate-800 mb-4">Lesson Notes</h2>
          <textarea {...register("notes")} rows={4} className="w-full px-3 py-2 border rounded-lg focus:ring-2" />
        </div>

        <div className="flex justify-end">
          <Button type="submit" disabled={isSubmitting} className="inline-flex items-center bg-blue-600 px-6 py-2 text-white rounded-lg font-medium hover:bg-blue-700">
            {isSubmitting ? (lesson ? "Saving changes..." : "Creating...") : (lesson ? "Update Lesson" : "Create Lesson")}
          </Button>
        </div>
      </div>
    </form>
  );
};