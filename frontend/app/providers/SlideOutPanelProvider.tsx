import {
  createContext,
  useContext,
  useState,
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
  const [onConfirm, setOnConfirm] = useState<(() => Promise<void>) | undefined>();

  const openPanel = ({ title, content, onConfirm }: SlideOutOptions) => {
    setTitle(title);
    setContent(content);
    setOnConfirm(() => onConfirm);
    setOpen(true);
  };

  const closePanel = () => setOpen(false);

  return (
    <SlideOutContext.Provider value={{ openPanel, closePanel }}>
      {children}
      <SlideOutPanel
        title={title}
        isOpen={isOpen}
        onClose={closePanel}
        onConfirm={onConfirm}
      >
        {content}
      </SlideOutPanel>
    </SlideOutContext.Provider>
  );
};