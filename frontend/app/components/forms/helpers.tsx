import { useFieldArray, type UseFormRegister } from "react-hook-form";

export function ArrayFieldSection({
    name,
    label,
    control,
    register,
    placeholder
}: {
    name: string;
    label: string;
    control: any;
    register: UseFormRegister<any>;
    placeholder?: string;
}) {
    const { fields, append, remove } = useFieldArray({ control, name });

    return (
        <div className="space-y-2">
            <label className="text-sm font-medium text-slate-700">{label}</label>
            {fields.map((field, index) => (
                <div key={field.id} className="flex relative items-center">
                    <input
                        {...register(`${name}.${index}.value`)}
                        defaultValue={field.value}
                        placeholder={placeholder}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                    {index !== 0 && (
                        <button
                            type="button"
                            onClick={() => remove(index)}
                            disabled={fields.length === 1}
                            className="p-2 px-3 text-red-600 absolute right-0 rounded-full outline-none focus:text-red-800 hover:text-red-800 cursor-pointer"
                        >
                            <span className="fa fa-fw fa-xmark"></span>
                        </button>
                    )}
                </div>
            ))}
            <button
                type="button"
                onClick={() => append({ value: "" })}
                className="text-navy-blue hover:text-blue-800 text-sm font-medium"
            >
                + Add {label.toLowerCase()}
            </button>
        </div>
    );
}