import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import api from '@/lib/api';
import type { components } from '@/types/api.d';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

type Class = components['schemas']['Class'];

interface ClassManagementDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onClassesUpdated: () => void;
}

export default function ClassManagementDialog({
  open,
  onOpenChange,
  onClassesUpdated,
}: ClassManagementDialogProps) {
  const { user } = useAuth();
  const [availableClasses, setAvailableClasses] = useState<Class[]>([]);
  const [enrolledClassIds, setEnrolledClassIds] = useState<Set<string>>(new Set());
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState('');

  // Fetch available classes when dialog opens
  useEffect(() => {
    if (open && user) {
      fetchClasses();
    }
  }, [open, user]);

  const fetchClasses = async () => {
    if (!user) return;

    setIsLoading(true);
    setError('');

    try {
      // Fetch all classes
      const classesResponse = await api.GET('/api/classes/');

      if (classesResponse.error) {
        setError('Failed to load classes');
        return;
      }

      if (classesResponse.data) {
        // Filter to only show classes from user's university
        const userClasses = user.university_id
          ? classesResponse.data.filter(
              (c) => c.university_id === user.university_id
            )
          : classesResponse.data;
        setAvailableClasses(userClasses);
      }

      // Fetch user's enrolled classes
      const enrolledResponse = await api.GET('/api/users/{user_id}/classes', {
        params: {
          path: {
            user_id: user.id,
          },
        },
      });

      if (enrolledResponse.data) {
        const enrolledIds = new Set(
          enrolledResponse.data.map((c) => c.id as string)
        );
        setEnrolledClassIds(enrolledIds);
      }
    } catch (err) {
      console.error('Error fetching classes:', err);
      setError('Failed to load classes');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    if (!user) return;

    setIsSaving(true);
    setError('');

    try {
      const classIds = Array.from(enrolledClassIds);

      const response = await api.PUT('/api/users/{user_id}/classes', {
        params: {
          path: {
            user_id: user.id,
          },
        },
        body: {
          class_ids: classIds,
        },
      });

      if (response.error) {
        setError('Failed to update classes');
        return;
      }

      onClassesUpdated();
      onOpenChange(false);
    } catch (err) {
      console.error('Error updating classes:', err);
      setError('Failed to update classes');
    } finally {
      setIsSaving(false);
    }
  };

  const toggleClass = (classId: string) => {
    setEnrolledClassIds((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(classId)) {
        newSet.delete(classId);
      } else {
        newSet.add(classId);
      }
      return newSet;
    });
  };

  const filteredClasses = availableClasses.filter((c) =>
    c.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[80vh] flex flex-col">
        <DialogHeader>
          <DialogTitle>Manage My Classes</DialogTitle>
          <DialogDescription>
            Select the classes you're currently enrolled in
          </DialogDescription>
        </DialogHeader>

        <div className="flex-1 overflow-y-auto space-y-4">
          {/* Search */}
          <div>
            <Label htmlFor="search">Search Classes</Label>
            <Input
              id="search"
              type="text"
              placeholder="Search by class name..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          {/* Class List */}
          {isLoading ? (
            <div className="text-center py-8 text-muted-foreground">
              Loading classes...
            </div>
          ) : filteredClasses.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              {searchQuery
                ? 'No classes match your search'
                : 'No classes available'}
            </div>
          ) : (
            <div className="space-y-2 max-h-96 overflow-y-auto border rounded-md p-4">
              {filteredClasses.map((classItem) => (
                <div
                  key={classItem.id}
                  className="flex items-center space-x-2 py-2 hover:bg-muted/50 rounded px-2"
                >
                  <Checkbox
                    id={`class-${classItem.id}`}
                    checked={enrolledClassIds.has(classItem.id as string)}
                    onCheckedChange={() => toggleClass(classItem.id as string)}
                  />
                  <Label
                    htmlFor={`class-${classItem.id}`}
                    className="flex-1 cursor-pointer"
                  >
                    <div className="font-medium">{classItem.name}</div>
                    {classItem.tags && classItem.tags.length > 0 && (
                      <div className="flex gap-1 mt-1">
                        {classItem.tags.map((tag) => (
                          <span
                            key={tag.id}
                            className="text-xs px-2 py-0.5 bg-primary/10 text-primary rounded-full"
                          >
                            {tag.name}
                          </span>
                        ))}
                      </div>
                    )}
                  </Label>
                </div>
              ))}
            </div>
          )}

          {error && (
            <div className="text-sm text-red-600 bg-red-50 p-3 rounded-md border border-red-200">
              {error}
            </div>
          )}

          <div className="text-sm text-muted-foreground">
            {enrolledClassIds.size} {enrolledClassIds.size === 1 ? 'class' : 'classes'} selected
          </div>
        </div>

        <DialogFooter>
          <Button
            variant="outline"
            onClick={() => onOpenChange(false)}
            disabled={isSaving}
          >
            Cancel
          </Button>
          <Button onClick={handleSave} disabled={isSaving || isLoading}>
            {isSaving ? 'Saving...' : 'Save Changes'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
