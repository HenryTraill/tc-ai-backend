import { href, Link } from "react-router";

export const Button = ({
  href = "#",
  icon,
  children = "Click me",
}: {
  href?: string;
  icon?: string;
  children?: React.ReactNode;
}) => {
  return <Link className="inline-flex items-center bg-steel-blue px-4 py-2 text-white rounded-lg font-medium transition-all"
    to={href}
    data-discover="true">{children}<span className={`ml-2 fa-fw ${icon} text-lg`}></span></Link>;
}