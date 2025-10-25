import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import ClassManagementDialog from '@/components/ClassManagementDialog';
import api from '@/lib/api';
import type { components } from '@/types/api.d';

type Class = components['schemas']['Class'];

export default function Profile() {
  const { user, updateUser, logout } = useAuth();
  const [name, setName] = useState(user?.name || '');
  const [isEditingName, setIsEditingName] = useState(false);
  const [isSavingName, setIsSavingName] = useState(false);
  const [nameError, setNameError] = useState('');
  const [nameSuccess, setNameSuccess] = useState('');

  // Password change dialog state
  const [isPasswordDialogOpen, setIsPasswordDialogOpen] = useState(false);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [passwordSuccess, setPasswordSuccess] = useState('');
  const [isSavingPassword, setIsSavingPassword] = useState(false);

  // Class management state
  const [enrolledClasses, setEnrolledClasses] = useState<Class[]>([]);
  const [isClassDialogOpen, setIsClassDialogOpen] = useState(false);
  const [isLoadingClasses, setIsLoadingClasses] = useState(true);

  if (!user) return null;

  // Fetch enrolled classes
  useEffect(() => {
    if (user) {
      fetchEnrolledClasses();
    }
  }, [user]);

  const fetchEnrolledClasses = async () => {
    if (!user) return;

    setIsLoadingClasses(true);
    try {
      const response = await api.GET('/api/users/{user_id}/classes', {
        params: {
          path: {
            user_id: user.id,
          },
        },
      });

      if (response.data) {
        setEnrolledClasses(response.data);
      }
    } catch (error) {
      console.error('Failed to fetch enrolled classes:', error);
    } finally {
      setIsLoadingClasses(false);
    }
  };

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  const handleNameUpdate = async () => {
    if (!name.trim()) {
      setNameError('Name cannot be empty');
      return;
    }

    setNameError('');
    setNameSuccess('');
    setIsSavingName(true);

    const result = await updateUser(user.id, { name: name.trim() });

    if (result.success) {
      setNameSuccess('Name updated successfully!');
      setIsEditingName(false);
      setTimeout(() => setNameSuccess(''), 3000);
    } else {
      setNameError(result.error || 'Failed to update name');
    }

    setIsSavingName(false);
  };

  const handlePasswordUpdate = async () => {
    setPasswordError('');
    setPasswordSuccess('');

    if (!newPassword || !confirmPassword) {
      setPasswordError('Please fill in all password fields');
      return;
    }

    if (newPassword !== confirmPassword) {
      setPasswordError('New passwords do not match');
      return;
    }

    if (newPassword.length < 6) {
      setPasswordError('Password must be at least 6 characters');
      return;
    }

    setIsSavingPassword(true);

    const result = await updateUser(user.id, { password: newPassword });

    if (result.success) {
      setPasswordSuccess('Password updated successfully!');
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
      setTimeout(() => {
        setPasswordSuccess('');
        setIsPasswordDialogOpen(false);
      }, 2000);
    } else {
      setPasswordError(result.error || 'Failed to update password');
    }

    setIsSavingPassword(false);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Profile Header Card */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-4">
            <Avatar className="h-20 w-20">
              <AvatarFallback className="text-2xl">
                {getInitials(user.name)}
              </AvatarFallback>
            </Avatar>
            <div>
              <CardTitle>{user.name}</CardTitle>
              <CardDescription>{user.email}</CardDescription>
              {user.university && (
                <p className="text-sm text-muted-foreground mt-1">
                  {user.university}
                </p>
              )}
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Edit Profile Card */}
      <Card>
        <CardHeader>
          <CardTitle>Edit Profile</CardTitle>
          <CardDescription>Update your account information</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Name Update */}
          <div className="space-y-2">
            <Label htmlFor="name">Name</Label>
            {isEditingName ? (
              <div className="space-y-2">
                <Input
                  id="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Enter your name"
                />
                {nameError && (
                  <p className="text-sm text-red-600">{nameError}</p>
                )}
                <div className="flex gap-2">
                  <Button
                    onClick={handleNameUpdate}
                    disabled={isSavingName}
                    size="sm"
                  >
                    {isSavingName ? 'Saving...' : 'Save'}
                  </Button>
                  <Button
                    onClick={() => {
                      setIsEditingName(false);
                      setName(user.name);
                      setNameError('');
                    }}
                    variant="outline"
                    size="sm"
                  >
                    Cancel
                  </Button>
                </div>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Input id="name" value={user.name} disabled />
                <Button
                  onClick={() => setIsEditingName(true)}
                  variant="outline"
                  size="sm"
                >
                  Edit
                </Button>
              </div>
            )}
            {nameSuccess && (
              <p className="text-sm text-green-600">{nameSuccess}</p>
            )}
          </div>

          {/* Email (Read-only) */}
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" value={user.email} disabled />
            <p className="text-sm text-muted-foreground">
              Email cannot be changed
            </p>
          </div>

          {/* University (Read-only) */}
          {user.university && (
            <div className="space-y-2">
              <Label htmlFor="university">University</Label>
              <Input id="university" value={user.university} disabled />
            </div>
          )}

          {/* Password Change Dialog */}
          <div className="space-y-2">
            <Label>Password</Label>
            <Dialog open={isPasswordDialogOpen} onOpenChange={setIsPasswordDialogOpen}>
              <DialogTrigger asChild>
                <Button variant="outline" className="w-full">
                  Change Password
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Change Password</DialogTitle>
                  <DialogDescription>
                    Update your account password
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4 py-4">
                  <div className="space-y-2">
                    <Label htmlFor="current-password">Current Password</Label>
                    <Input
                      id="current-password"
                      type="password"
                      value={currentPassword}
                      onChange={(e) => setCurrentPassword(e.target.value)}
                      placeholder="Enter current password"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="new-password">New Password</Label>
                    <Input
                      id="new-password"
                      type="password"
                      value={newPassword}
                      onChange={(e) => setNewPassword(e.target.value)}
                      placeholder="Enter new password"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="confirm-password">Confirm New Password</Label>
                    <Input
                      id="confirm-password"
                      type="password"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      placeholder="Confirm new password"
                    />
                  </div>
                  {passwordError && (
                    <p className="text-sm text-red-600">{passwordError}</p>
                  )}
                  {passwordSuccess && (
                    <p className="text-sm text-green-600">{passwordSuccess}</p>
                  )}
                </div>
                <DialogFooter>
                  <Button
                    variant="outline"
                    onClick={() => {
                      setIsPasswordDialogOpen(false);
                      setCurrentPassword('');
                      setNewPassword('');
                      setConfirmPassword('');
                      setPasswordError('');
                    }}
                  >
                    Cancel
                  </Button>
                  <Button
                    onClick={handlePasswordUpdate}
                    disabled={isSavingPassword}
                  >
                    {isSavingPassword ? 'Updating...' : 'Update Password'}
                  </Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </div>
        </CardContent>
      </Card>

      {/* My Classes Card */}
      <Card>
        <CardHeader>
          <CardTitle>My Classes</CardTitle>
          <CardDescription>
            Classes you're currently enrolled in
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {isLoadingClasses ? (
            <div className="text-center py-4 text-muted-foreground">
              Loading classes...
            </div>
          ) : enrolledClasses.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground border-2 border-dashed rounded-md">
              <p>No classes enrolled yet</p>
              <p className="text-sm mt-1">Click "Manage Classes" to get started</p>
            </div>
          ) : (
            <div className="space-y-2">
              {enrolledClasses.map((classItem) => (
                <div
                  key={classItem.id}
                  className="p-3 border rounded-md hover:bg-muted/50"
                >
                  <div className="font-medium">{classItem.name}</div>
                  {classItem.tags && classItem.tags.length > 0 && (
                    <div className="flex gap-1 mt-2">
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
                </div>
              ))}
            </div>
          )}

          <Button
            onClick={() => setIsClassDialogOpen(true)}
            variant="outline"
            className="w-full"
          >
            Manage Classes
          </Button>
        </CardContent>
      </Card>

      {/* Logout Card */}
      <Card>
        <CardContent className="pt-6">
          <Button
            onClick={logout}
            variant="destructive"
            className="w-full"
          >
            Logout
          </Button>
        </CardContent>
      </Card>

      {/* Class Management Dialog */}
      <ClassManagementDialog
        open={isClassDialogOpen}
        onOpenChange={setIsClassDialogOpen}
        onClassesUpdated={fetchEnrolledClasses}
      />
    </div>
  );
}
