import { useForm } from "react-hook-form";
import { useNavigate } from "react-router";
import { lessonsApi, type Lesson, type Student } from "../../data/api";
import { Button } from "../ui/Button";
import { fullName } from "~/helpers/students";
import { SlideOutPanelFooter } from "../SlideOutPanel";
import { useRef, type RefObject } from "react";
import { formatTimeForInput } from "~/helpers/lessons";

interface LessonFormValues {
  student_id: string;
  date: string;
  start_time: string;
  end_time: string;
  subject: string;
  topic: string;
  notes: string;
  status: 'planned' | 'complete' | 'pending' | 'cancelled' | 'cancelled-but-chargeable',
  skills_practiced: { value: string }[];
  main_subjects_covered: { value: string }[];
  student_strengths_observed: { value: string }[];
  student_weaknesses_observed: { value: string }[];
  tutor_tips: { value: string }[];
}

type LessonFormProps = {
  students: Student[];
  lesson?: Lesson;
};

export const LessonForm = ({ students, lesson }: LessonFormProps) => {
  const navigate = useNavigate();
  const formRef: RefObject<HTMLFormElement | null> = useRef(null);

  const {
    register,
    handleSubmit,
    formState: { isSubmitting },
  } = useForm<LessonFormValues>({
    defaultValues: {
      student_id: lesson?.student_id?.toString() ?? "",
      date: lesson?.start_dt ? lesson.start_dt.slice(0, 10) : "",
      start_time: lesson?.start_dt ? formatTimeForInput(lesson.start_dt) : "",
      end_time: lesson?.end_dt ? formatTimeForInput(lesson.end_dt) : "",
      subject: lesson?.subject ?? "",
      topic: lesson?.topic ?? "",
      notes: lesson?.notes ?? "",
      status: lesson?.status ?? 'planned',
      skills_practiced: lesson?.skills_practiced?.map((v) => ({ value: v })) ?? [{ value: "" }],
      main_subjects_covered: lesson?.main_subjects_covered?.map((v) => ({ value: v })) ?? [{ value: "" }],
      student_strengths_observed: lesson?.student_strengths_observed?.map((v) => ({ value: v })) ?? [{ value: "" }],
      student_weaknesses_observed: lesson?.student_weaknesses_observed?.map((v) => ({ value: v })) ?? [{ value: "" }],
      tutor_tips: lesson?.tutor_tips?.map((v) => ({ value: v })) ?? [{ value: "" }],
    },
  });

  const onSubmit = async (data: LessonFormValues) => {
    const start_dt = new Date(`${data.date}T${data.start_time}`);
    const end_dt = new Date(`${data.date}T${data.end_time}`);

    const payload = {
      student_id: parseInt(data.student_id),
      start_dt: start_dt.toISOString(),
      end_dt: end_dt.toISOString(),
      subject: data.subject,
      topic: data.topic,
      notes: data.notes,
      status: lesson?.status ?? "planned",
      skills_practiced: data.skills_practiced.map((i) => i.value).filter(Boolean),
      main_subjects_covered: data.main_subjects_covered.map((i) => i.value).filter(Boolean),
      student_strengths_observed: data.student_strengths_observed.map((i) => i.value).filter(Boolean),
      student_weaknesses_observed: data.student_weaknesses_observed.map((i) => i.value).filter(Boolean),
      tutor_tips: data.tutor_tips.map((i) => i.value).filter(Boolean),
    };

    const response = lesson
      ? await lessonsApi.update(lesson.id, payload)
      : await lessonsApi.create(payload);

    if (response) {
      navigate(0);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} ref={formRef}>
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="flex flex-col p-4 gap-4">
          <div>
            <label className="text-sm font-medium text-slate-700 mb-1 block">Student</label>
            <select
              {...register("student_id")}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2"
            >
              <option value="">Select a student</option>
              {students.map((student) => (
                <option key={student.id} value={student.id}>
                  {fullName(student)}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-sm font-medium text-slate-700 mb-1 block">Date</label>
            <input
              type="date"
              {...register("date")}
              required
              className="w-full px-3 py-2 border rounded-lg focus:ring-2"
            />
          </div>

          <div>
            <label className="text-sm font-medium text-slate-700 mb-1 block">Start Time</label>
            <input
              type="time"
              {...register("start_time")}
              required
              className="w-full px-3 py-2 border rounded-lg focus:ring-2"
            />
          </div>

          <div>
            <label className="text-sm font-medium text-slate-700 mb-1 block">End Time</label>
            <input
              type="time"
              {...register("end_time")}
              required
              className="w-full px-3 py-2 border rounded-lg focus:ring-2"
            />
          </div>

          <div>
            <label className="text-sm font-medium text-slate-700 mb-1 block">Subject</label>
            <input
              type="text"
              {...register("subject")}
              required
              className="w-full px-3 py-2 border rounded-lg focus:ring-2"
            />
          </div>

          <div>
            <label className="text-sm font-medium text-slate-700 mb-1 block">Status</label>
            <select
              {...register("status")}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2"
            >
              <option value="planned">Planned</option>
              <option value="pending">Pending</option>
              <option value="complete">Complete</option>
              <option value="cancelled">Cancelled</option>
              <option value="cancelled-but-chargeable">Cancelled but chargeable</option>
            </select>
          </div>

          <div>
            <label className="text-sm font-medium text-slate-700 mb-1 block">Topic</label>
            <input
              type="text"
              {...register("topic")}
              required
              className="w-full px-3 py-2 border rounded-lg focus:ring-2"
            />
          </div>

          <div>
            <label className="text-sm font-medium text-slate-700 mb-1 block">Notes</label>
            <textarea
              {...register("notes")}
              rows={4}
              className="w-full px-3 py-2 border rounded-lg focus:ring-2"
            />
          </div>
        </div>
      </div>

      <SlideOutPanelFooter>
        <Button type="submit" disabled={isSubmitting} onClick={() => formRef?.current?.requestSubmit()}>
          {isSubmitting
            ? lesson
              ? "Saving changes..."
              : "Creating..."
            : lesson
              ? "Update Lesson"
              : "Create Lesson"}
        </Button>
      </SlideOutPanelFooter>
    </form>
  );
};