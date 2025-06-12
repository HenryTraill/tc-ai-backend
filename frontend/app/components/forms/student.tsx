import { useForm } from "react-hook-form";
import { useNavigate } from "react-router";
import { clientsApi, studentsApi, type Client, type Student } from "../../data/api";
import { Button } from "../ui/Button";
import { useEffect, useRef, useState, type RefObject } from "react";
import { SlideOutPanelFooter } from "../SlideOutPanel";
import { fullName } from "~/helpers/students";

type StudentFormProps = {
  student?: Student;
};

export const StudentForm = ({ student }: StudentFormProps) => {
  const formRef: RefObject<HTMLFormElement | null> = useRef(null);
  const [clients, setClients] = useState<Client[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();


  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const clientData = await clientsApi.getAll()
        setClients(clientData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch student data');
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [])

  const {
    register,
    handleSubmit,
    formState: { isSubmitting }
  } = useForm({
    defaultValues: {
      client_id: student?.client_id?.toString() ?? '',
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
      navigate(0); // Refresh the page to show updated data
    }
  };

  if (loading) {
    return (
      <div className="p-8 min-h-full bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-slate-800 mx-auto mb-4"></div>
          <p className="text-slate-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <form ref={formRef} onSubmit={handleSubmit(onSubmit)}>
        <div className="p-4 space-y-4">
          <div className="grid gap-4">
            <div>
              <label className="text-sm font-medium text-slate-700 mb-1 block">Client</label>
              <select
                {...register("client_id", {
                  required: true,
                  valueAsNumber: true, // 💡 This tells react-hook-form to treat the value as a number
                })}

              >
                <option value="">Select a Client</option>
                {clients.map((client) => (
                  <option key={client.id} value={client.id}>
                    {fullName(client)}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-sm font-medium text-slate-700 mb-1 block">First Name</label>
              <input type="text" {...register("first_name")} required />
            </div>
            <div>
              <label className="text-sm font-medium text-slate-700 mb-1 block">Last Name</label>
              <input type="text" {...register("last_name")} required />
            </div>
            <div>
              <label className="text-sm font-medium text-slate-700 mb-1 block">Email</label>
              <input type="email" {...register("email")} required />
            </div>
            <div>
              <label className="text-sm font-medium text-slate-700 mb-1 block">Phone</label>
              <input type="tel" {...register("phone")} required />
            </div>
            <div>
              <label className="text-sm font-medium text-slate-700 mb-1 block">Grade</label>
              <input type="text" {...register("grade")} required />
            </div>
          </div>
        </div>
      </form>
      <SlideOutPanelFooter>
        <Button type="submit" disabled={isSubmitting} onClick={() => formRef?.current?.requestSubmit()}>
          {student ? "Update Student" : "Create Student"}
        </Button>
      </SlideOutPanelFooter>
    </>
  );
};