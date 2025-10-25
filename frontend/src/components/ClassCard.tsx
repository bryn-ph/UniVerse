import { Link, useNavigate } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { TagList } from "@/components/Tag";
import type { components } from "@/types/api.d";
import ShareMenu from "./ShareMenu";

type Tag = components["schemas"]["TagMini"];

interface ClassCardProps {
  id: string;
  title: string;
  subtitle: string;
  count: number;
  countLabel?: string; // "discussion" or "class"
  tags?: Tag[];
  linkTo: string;
  badge?: string; // Optional badge (e.g., "3 classes" for groups)
  linkState?: any; // Optional state to pass to React Router
}

export default function ClassCard({
  id,
  title,
  subtitle,
  count,
  countLabel = "discussion",
  tags,
  linkTo,
  badge,
}: ClassCardProps) {
  const navigate = useNavigate();
  const classLink = linkTo || `/classes/${id}`;
  const handleCardClick = () => {
    navigate(classLink);
  };
  return (
    <Card
        className="hover:shadow-lg transition-shadow cursor-pointer h-full relative"
        onClick={handleCardClick}
    >
        <CardHeader>
            <div className="flex items-start justify-between">
            <div className="flex-1">
                <CardTitle className="text-xl">{title}</CardTitle>
                <CardDescription className="text-sm">{subtitle}</CardDescription>
            </div>
            {badge && (
                <span className="px-2 py-1 text-xs font-semibold bg-blue-100 text-blue-800 rounded-full">
                {badge}
                </span>
            )}
            </div>
        </CardHeader>
        <CardContent className="space-y-3">
            {/* Count */}
            <div className="flex items-center text-sm text-muted-foreground">
                <svg
                className="w-4 h-4 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                >
                <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                />
                </svg>
            {`${count} ${count === 1 ? countLabel === "discussion" ? "discussion" : "class" : countLabel === "discussion" ? "discussions" : "classes"}`}
            </div>

            {/* Tags */}
            <TagList tags={tags || []} variant="primary" />
        </CardContent>
                {/* ShareMenu positioned absolutely */}
        <div className="absolute top-3 right-3">
            <ShareMenu path={classLink} />
        </div>
    </Card>
  );
}
