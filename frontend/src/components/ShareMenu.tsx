import * as React from "react";
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from "./ui/dropdown-menu";

type ShareMenuProps = {
  /** The href path (relative) to the resource, e.g. `/discussions/123` */
  path: string;
  /** Optional aria label for the trigger */
  ariaLabel?: string;
  /** Optional className to apply to trigger button */
  className?: string;
};

export default function ShareMenu({ path, ariaLabel = "Share actions", className = "" }: ShareMenuProps) {
  const [copied, setCopied] = React.useState(false);

  const handleCopy = async () => {
    const link = `${window.location.origin}${path}`;
    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(link);
      } else {
        const ta = document.createElement("textarea");
        ta.value = link;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        document.body.removeChild(ta);
      }
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (e) {
      console.error("Copy failed", e);
    }
  };

  return (
    <div className={`relative ${className}`}>
      <DropdownMenu>
        <DropdownMenuTrigger>
          <div className="h-8 w-8 rounded-md bg-muted/20 flex items-center justify-center text-muted-foreground hover:bg-muted/30 transition-colors cursor-pointer">
            <span className="text-xs">•••</span>
          </div>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem onClick={() => handleCopy()}>Copy link</DropdownMenuItem>
          <DropdownMenuItem
            onClick={() => {
              const url = `${window.location.origin}${path}`;
              window.open(url, "_blank");
            }}
          >
            Open in new tab
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      {copied && (
        <div className="absolute -top-8 right-0 px-2 py-1 rounded text-xs bg-green-600 text-white">Link copied</div>
      )}
    </div>
  );
}
