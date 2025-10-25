import type { components } from "@/types/api.d";

type TagMini = components["schemas"]["TagMini"];

interface TagProps {
  tag: TagMini;
  variant?: "primary" | "muted";
}

export default function Tag({ tag, variant = "primary" }: TagProps) {
  const baseClasses = "inline-flex items-center rounded-full text-xs font-medium";
  
  const variantClasses = variant === "primary" 
    ? "px-2 py-1 bg-primary/10 text-primary"
    : "px-2 py-0.5 bg-muted/40 text-muted-foreground";

  return (
    <span className={`${baseClasses} ${variantClasses}`}>
      {tag.name}
    </span>
  );
}

interface TagListProps {
  tags?: any;
  variant?: "primary" | "muted";
  className?: string;
}

export function TagList({ tags, variant = "primary", className = "" }: TagListProps) {
  if (!tags || tags.length === 0) return null;

  return (
    <div className={`flex flex-wrap gap-2 ${className}`}>
      {tags.filter((tag: any) => tag != null).map((tag: any) => (
        <Tag key={tag.id} tag={tag} variant={variant} />
      ))}
    </div>
  );
}
