import { useForm } from "react-hook-form";
import { useNavigate } from "react-router";
import { studentsApi } from "../../data/api";
import { Button } from "../ui/Button";

interface StudentFormData {
  id?: number;
  client_id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  grade: string;
  strengths: string[];
  weaknesses: string[];
}

type StudentFormProps = {
  student?: StudentFormData;
};

export const StudentForm = ({ student }: StudentFormProps) => {
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { isSubmitting }
  } = useForm({
    defaultValues: {
      client_id: student?.client_id ?? 0,
      first_name: student?.first_name ?? '',
      last_name: student?.last_name ?? '',
      email: student?.email ?? '',
      phone: student?.phone ?? '',
      grade: student?.grade ?? '',
    }
  });

  const onSubmit = async (data: any) => {
    const response = student
      ? await studentsApi.update(student.id!, data)
      : await studentsApi.create(data);

    if (response) {
      navigate("/students");
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div className="bg-white border shadow-sm p-6 rounded-xl">
        <h2 className="text-xl font-semibold text-slate-800 mb-4">Student Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium text-slate-700 mb-1 block">Client ID</label>
            <input type="number" {...register("client_id")} required className="w-full px-3 py-2 border rounded-lg focus:ring-2" />
          </div>
          <div>
            <label className="text-sm font-medium text-slate-700 mb-1 block">First Name</label>
            <input type="text" {...register("first_name")} required className="w-full px-3 py-2 border rounded-lg focus:ring-2" />
          </div>
          <div>
            <label className="text-sm font-medium text-slate-700 mb-1 block">Last Name</label>
            <input type="text" {...register("last_name")} required className="w-full px-3 py-2 border rounded-lg focus:ring-2" />
          </div>
          <div>
            <label className="text-sm font-medium text-slate-700 mb-1 block">Email</label>
            <input type="email" {...register("email")} required className="w-full px-3 py-2 border rounded-lg focus:ring-2" />
          </div>
          <div>
            <label className="text-sm font-medium text-slate-700 mb-1 block">Phone</label>
            <input type="tel" {...register("phone")} required className="w-full px-3 py-2 border rounded-lg focus:ring-2" />
          </div>
          <div className="md:col-span-2">
            <label className="text-sm font-medium text-slate-700 mb-1 block">Grade</label>
            <input type="text" {...register("grade")} required className="w-full px-3 py-2 border rounded-lg focus:ring-2" />
          </div>
        </div>
      </div>
      <div className="flex justify-end">
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? (student ? "Saving changes..." : "Creating...") : (student ? "Update Student" : "Create Student")}
        </Button>
      </div>
    </form>
  );
};