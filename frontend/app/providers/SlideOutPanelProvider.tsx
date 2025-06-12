import {
  createContext,
  useContext,
  useState,
  useEffect,
  type ReactNode,
} from "react";
import { SlideOutPanel } from "~/components/SlideOutPanel";

type SlideOutOptions = {
  title: string;
  content: ReactNode;
  onConfirm?: () => Promise<void>;
};

type SlideOutPanelContextType = {
  openPanel: (options: SlideOutOptions) => void;
  closePanel: () => void;
};

const SlideOutContext = createContext<SlideOutPanelContextType | undefined>(undefined);

export const useSlideOutPanel = (): SlideOutPanelContextType => {
  const context = useContext(SlideOutContext);
  if (!context) {
    throw new Error("useSlideOut must be used within a SlideOutProvider");
  }
  return context;
};

export const SlideOutProvider = ({ children }: { children: ReactNode }) => {
  const [isOpen, setOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState<ReactNode>(null);

  const openPanel = ({ title, content }: SlideOutOptions) => {
    setTitle(title);
    setContent(content);
    setOpen(true);
  };

  const closePanel = () => setOpen(false);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        closePanel();
      }
    };

    if (isOpen) {
      window.addEventListener("keydown", handleKeyDown);
    } else {
      window.removeEventListener("keydown", handleKeyDown);
    }

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen]);

  return (
    <SlideOutContext.Provider value={{ openPanel, closePanel }}>
      {children}
      <SlideOutPanel
        title={title}
        isOpen={isOpen}
        onClose={closePanel}
      >
        {content}
      </SlideOutPanel>
    </SlideOutContext.Provider>
  );
};