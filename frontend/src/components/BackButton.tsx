import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import type { ReactNode } from "react";

interface BackButtonProps {
  to?: string;
  onClick?: () => void;
  children?: ReactNode;
  /** If true, use the filled primary style (same blue used elsewhere) */
  primary?: boolean;
  size?: "sm" | "lg" | "default";
  className?: string;
}

export default function BackButton({
  to,
  onClick,
  children,
  primary = false,
  size = "sm",
  className = "",
}: BackButtonProps) {
  const content = children ?? "← Back";
  // Primary uses the same blue used in other places in the app
  const primaryClasses = "bg-[#234E70] text-white hover:bg-[#1d3f56] hover:cursor-pointer";

  const btn = (
    <Button
      variant={primary ? "default" : "ghost"}
      size={size}
      onClick={onClick}
      className={`${primary ? primaryClasses : "hover:cursor-pointer"} ${className}`.trim()}
    >
      {content}
    </Button>
  );

  return to ? <Link to={to}>{btn}</Link> : btn;
}
