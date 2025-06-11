import { useForm, useFieldArray, type UseFormRegister } from "react-hook-form";
import { lessonsApi, type Student } from "../../../data/api";
import { useNavigate } from "react-router";
import { ArrayFieldSection } from "../helpers";

export const LessonForm = ({ students }: { students: Student[] }) => {
    const navigate = useNavigate();
    const {
        register,
        handleSubmit,
        control,
        formState: { isSubmitting }
    } = useForm({
        defaultValues: {
            student_id: '',
            date: '',
            start_time: '',
            subject: '',
            topic: '',
            duration: 60,
            notes: '',
            skills_practiced: [{ value: '' }],
            main_subjects_covered: [{ value: '' }],
            student_strengths_observed: [{ value: '' }],
            student_weaknesses_observed: [{ value: '' }],
            tutor_tips: [{ value: '' }]
        }
    });

    const onSubmit = async (data) => {
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

        const response = await lessonsApi.create(cleaned);
        if (response) {
            navigate("/lessons");
        }
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-8 min-h-full bg-cream">
            <div className="max-w-6xl mx-auto space-y-8">

                {/* Section: Basic Info */}
                <div className="bg-white border shadow-sm p-6 rounded-xl">
                    <h2 className="text-xl font-semibold text-slate-800 mb-4">Basic Information</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        <div>
                            <label className="text-sm font-medium text-slate-700 mb-1 block">Student</label>
                            <select {...register("student_id")} required className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                                <option value="">Select a student</option>
                                {students.map((student) => (
                                    <option key={student.id} value={student.id}>{student.name}</option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label className="text-sm font-medium text-slate-700 mb-1 block">Date</label>
                            <input type="date" {...register("date")} required className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2" />
                        </div>

                        <div>
                            <label className="text-sm font-medium text-slate-700 mb-1 block">Start Time</label>
                            <input type="time" {...register("start_time")} required className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2" />
                        </div>

                        <div>
                            <label className="text-sm font-medium text-slate-700 mb-1 block">Subject</label>
                            <input type="text" {...register("subject")} required placeholder="e.g., Mathematics" className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2" />
                        </div>

                        <div>
                            <label className="text-sm font-medium text-slate-700 mb-1 block">Topic</label>
                            <input type="text" {...register("topic")} required placeholder="e.g., Quadratic Equations" className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2" />
                        </div>

                        <div>
                            <label className="text-sm font-medium text-slate-700 mb-1 block">Duration (minutes)</label>
                            <input type="number" {...register("duration")} required min="1" className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2" />
                        </div>
                    </div>
                </div>

                {/* Notes */}
                <div className="bg-white border shadow-sm p-6 rounded-xl">
                    <h2 className="text-xl font-semibold text-slate-800 mb-4">Lesson Notes</h2>
                    <textarea {...register("notes")} rows={4} placeholder="General observations and engagement..." className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2" />
                </div>

                {/* Skills & Subjects */}
                <div className="bg-white border shadow-sm p-6 rounded-xl space-y-6">
                    <h2 className="text-xl font-semibold text-slate-800 mb-4">Skills & Subjects</h2>
                    <ArrayFieldSection name="skills_practiced" label="Skills Practiced" control={control} register={register} placeholder="e.g., Completing the square" />
                    <ArrayFieldSection name="main_subjects_covered" label="Main Subjects Covered" control={control} register={register} placeholder="e.g., Quadratic formula" />
                </div>

                {/* Assessment */}
                <div className="bg-white border shadow-sm p-6 rounded-xl space-y-6">
                    <h2 className="text-xl font-semibold text-slate-800 mb-4">Student Assessment</h2>
                    <ArrayFieldSection name="student_strengths_observed" label="Student Strengths Observed" control={control} register={register} placeholder="e.g., Strong mental math" />
                    <ArrayFieldSection name="student_weaknesses_observed" label="Student Weaknesses Observed" control={control} register={register} placeholder="e.g., Needs help with story problems" />
                </div>

                {/* Tips */}
                <div className="bg-white border shadow-sm p-6 rounded-xl space-y-6">
                    <h2 className="text-xl font-semibold text-slate-800 mb-4">Tutor Recommendations</h2>
                    <ArrayFieldSection name="tutor_tips" label="Tutor Tips" control={control} register={register} placeholder="e.g., Use visual aids" />
                </div>

                {/* Submit */}
                <div className="flex justify-end">
                    <button type="submit" disabled={isSubmitting} className="inline-flex items-center bg-steel-blue px-4 py-2 text-white rounded-lg font-medium">
                        {isSubmitting ? "Saving..." : "Create Lesson"}
                    </button>
                </div>

            </div>
        </form>
    );
};