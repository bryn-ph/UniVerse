import { Badge, badgeVariants } from "@/components/ui/badge";
import type { components } from "@/types/api.d";
import type { VariantProps } from "class-variance-authority";

type TagMini = components["schemas"]["TagMini"];

interface TagProps {
  tag: TagMini;
  variant?: "primary" | "muted" | "secondary" | "destructive" | "outline";
}

export default function Tag({ tag, variant = "primary" }: TagProps) {
  return (
    <Badge variant={variant as VariantProps<typeof badgeVariants>["variant"]} className="text-sm mt-2 text-muted-foreground hover:bg-muted-foreground/10 hover:text-muted-foreground">
      {tag.name}
    </Badge>
  );
}

interface TagListProps {
  tags?: any;
  variant?: "primary" | "muted" | "secondary" | "destructive" | "outline";
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
