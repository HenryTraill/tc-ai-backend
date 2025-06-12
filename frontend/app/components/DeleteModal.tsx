import { useState } from "react";
import { useNavigate } from "react-router";
import { Button } from "./ui/Button";

type DeleteModalProps = {
  onConfirm: () => Promise<{ message: string; }>
  resourceName?: string;
  redirectTo?: string;
};

export const DeleteModal = ({
  onConfirm,
  resourceName = "item",
  redirectTo = "/",
}: DeleteModalProps) => {
  const [open, setOpen] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const navigate = useNavigate();

  const handleDelete = async () => {
    setDeleting(true);
    try {
      await onConfirm();
      navigate(redirectTo);
    } catch (err) {
      alert(`Failed to delete the ${resourceName}. Please try again.`);
    } finally {
      setDeleting(false);
    }
  };

  return (
    <>
      <Button
        onClick={() => setOpen(true)}
        icon="trash"
        variant="warning"
      >
        Delete {resourceName.charAt(0).toUpperCase() + resourceName.slice(1)}
      </Button>

      {open && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
            <h2 className="text-lg font-semibold text-slate-800 mb-4">
              Confirm Deletion
            </h2>
            <p className="text-slate-600 mb-6">
              Are you sure you want to delete this {resourceName}? This action cannot be undone.
            </p>
            <div className="flex justify-end gap-2">
              <button
                onClick={() => setOpen(false)}
                className="px-4 py-2 rounded-lg text-slate-700 border border-gray-300 hover:bg-gray-100"
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                disabled={deleting}
                className="px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-700 disabled:opacity-50"
              >
                {deleting ? "Deleting..." : `Yes, Delete ${resourceName}`}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};