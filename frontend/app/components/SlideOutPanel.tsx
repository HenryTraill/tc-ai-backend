import React, { useEffect, useState } from "react";

type SlideOutPanelProps = {
  title: string;
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
};

export const SlideOutPanelFooter = ({ children }: { children: React.ReactElement }) => {
  return (
    <div className="flex sticky bottom-0 justify-end p-4 border-t mt-auto bg-cream">
      {children}
    </div>
  );
}


export const SlideOutPanel = ({
  title,
  isOpen,
  onClose,
  children
}: SlideOutPanelProps) => {
  const [shouldRender, setShouldRender] = useState(isOpen);

  useEffect(() => {
    if (isOpen) {
      setShouldRender(true);
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
      const timeout = setTimeout(() => setShouldRender(false), 300); // match CSS transition
      return () => clearTimeout(timeout);
    }
  }, [isOpen]);

  return (
    <div
      className={`fixed inset-0 z-50 transition-all duration-300 ${isOpen ? "" : "pointer-events-none"
        }`}
    >
      <div
        className={`absolute inset-0 bg-black/40 transition-opacity ${isOpen ? "opacity-100" : "opacity-0"
          }`}
        onClick={onClose}
      />

      <div
        className={`absolute top-0 right-0 h-full w-full max-w-md shadow-xl transition-transform duration-300 ease-in-out bg-cream ${isOpen ? "translate-x-0" : "translate-x-full"
          }`}
      >
        <div className="flex justify-between items-center px-4 py-3 border-b">
          <h2 className="text-lg font-semibold text-slate-800">{title}</h2>
          <button
            onClick={onClose}
            className="text-slate-500 hover:text-slate-700 text-lg"
            aria-label="Close"
          >
            &times;
          </button>
        </div>

        <div className="overflow-scroll max-h-[calc(100vh-54px)] bg-white">
          {shouldRender ? children : null}
        </div>
      </div>
    </div>
  );
};