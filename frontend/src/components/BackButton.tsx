import { Link, useLocation } from "react-router-dom";
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
  /** If true, automatically determine back destination based on navigation history */
  autoBack?: boolean;
}

export default function BackButton({
  to,
  onClick,
  children,
  primary = false,
  size = "sm",
  className = "",
  autoBack = false,
}: BackButtonProps) {
  const location = useLocation();
  
  const getBackDestination = () => {
    if (autoBack) {
      // Check if we have navigation state from previous page
      const state = location.state as { from?: string; groupId?: string; groupName?: string } | null;
      
      if (state?.from === 'group' && state.groupId) {
        return {
          to: `/class-groups/${state.groupId}`,
          text: `← Back to ${state.groupName || 'Class Group'}`
        };
      }
      
      if (state?.from === 'home') {
        return {
          to: '/',
          text: '← Back to Home'
        };
      }
      
      if (state?.from === 'explore') {
        return {
          to: '/explore',
          text: '← Back to Explore'
        };
      }
      
      // Default fallback - always go to explore
      return {
        to: '/explore',
        text: '← Back to Explore'
      };
    }
    
    return {
      to: to,
      text: children ?? "← Back"
    };
  };

  const destination = getBackDestination();
  const content = destination.text;
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

  return destination.to ? <Link to={destination.to}>{btn}</Link> : btn;
}
