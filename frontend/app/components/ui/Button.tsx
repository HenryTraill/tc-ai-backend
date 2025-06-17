import { Link } from "react-router";

type ButtonProps = {
  href?: string;
  onClick?: () => void;
  icon?: string;
  children?: React.ReactNode;
  variant?: "primary" | "warning" | "success" | "outline" | "ghost";
  type?: "button" | "submit" | "reset";
  disabled?: boolean;
  loading?: boolean;
};

export const Button = ({
  href,
  onClick,
  icon,
  disabled = false,
  children = "",
  variant = "primary",
  type = "button",
  loading = false,
}: ButtonProps) => {
  const base =
    "inline-flex items-center px-4 py-2.5 rounded-lg font-medium transition-all cursor-pointer";
  let styles = "";

  if (disabled) {
    styles = "bg-gray-300 text-gray-500 cursor-not-allowed";
  } else {
    switch (variant) {
      case "primary":
        styles = "bg-steel-blue text-white hover:bg-navy-blue";
        break;
      case "warning":
        styles = "bg-red-700 text-white hover:bg-red-600";
        break;
      case "success":
        styles = "bg-green-500 text-white hover:bg-green-600";
        break;
      case "outline":
        styles =
          "border border-steel-blue text-steel-blue hover:bg-steel-blue hover:text-white";
        break;
      case "ghost":
        styles =
          "text-steel-blue bg-transparent";
        break;
      default:
        styles = "bg-steel-blue text-white hover:bg-blue-700";
    }
  }

  const content = (
    <>
      {children}
      {icon && (
        <span className={`ml-2 fa fa-fw fa-${icon} text-sm`}></span>
      )}
    </>
  );

  if (href) {
    return (
      <Link to={href} className={`${base} ${styles}`} data-discover="true">
        {content}
      </Link>
    );
  }

  return (
    <button
      type={type}
      onClick={onClick}
      className={`${base} ${styles}`}
      disabled={disabled}
    >
      {/* TODO REMOVE MARGIN FROM ICON WHEN NO TEXT PRESENT */}
      {loading ? (
        <span className="loader spinner-border animate-spin w-4 h-4 mr-2 border-2 border-white border-t-transparent rounded-full"></span>
      ) : (
        <>
          {children}
          {icon && (
            <span className={`ml-2 fa fa-fw fa-${icon} text-md`}></span>
          )}
        </>
      )}
    </button>
  );
};