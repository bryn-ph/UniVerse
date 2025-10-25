import * as React from "react";

const DropdownContext = React.createContext<{
  open: boolean;
  setOpen: (v: boolean) => void;
} | null>(null);

export function DropdownMenu({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = React.useState(false);
  return (
    <DropdownContext.Provider value={{ open, setOpen }}>
      <div className="relative inline-block">{children}</div>
    </DropdownContext.Provider>
  );
}

export function DropdownMenuTrigger({ children }: { children: React.ReactNode }) {
  const ctx = React.useContext(DropdownContext);
  if (!ctx) return null;
  const { open, setOpen } = ctx;
  return (
    <button
      onClick={(e) => {
        e.stopPropagation();
        setOpen(!open);
      }}
      className="inline-flex items-center justify-center"
    >
      {children}
    </button>
  );
}

export function DropdownMenuContent({ children }: { children: React.ReactNode }) {
  const ctx = React.useContext(DropdownContext);
  if (!ctx) return null;
  const { open } = ctx;
  if (!open) return null;
  return (
    <div className="absolute right-0 mt-2 w-44 z-50">
      <div className="rounded-md border bg-white shadow-md dark:bg-muted p-1">{children}</div>
    </div>
  );
}

export function DropdownMenuItem({ children, onClick }: { children: React.ReactNode; onClick?: (e: React.MouseEvent) => void }) {
  const ctx = React.useContext(DropdownContext);
  return (
    <button
      onClick={(e) => {
        e.stopPropagation();
        onClick?.(e);
        // close menu after click
        if (ctx) ctx.setOpen(false);
      }}
      className="w-full text-left px-3 py-2 text-sm hover:bg-slate-50 dark:hover:bg-slate-700 rounded"
    >
      {children}
    </button>
  );
}

export default DropdownMenu;
