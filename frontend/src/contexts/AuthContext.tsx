import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import api from '@/lib/api';

interface User {
  id: string;
  name: string;
  email: string;
  university: string | null;
  university_id?: string;
}

interface LoginResponse {
  message: string;
  user: {
    id: string;
    name: string;
    email: string;
    university: string | null;
  };
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<{ success: boolean; error?: string }>;
  signup: (name: string, email: string, password: string, universityId: string) => Promise<{ success: boolean; error?: string }>;
  logout: () => void;
  updateUser: (userId: string, data: { name?: string; password?: string }) => Promise<{ success: boolean; error?: string }>;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load user from localStorage on mount
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (e) {
        console.error('Failed to parse stored user:', e);
        localStorage.removeItem('user');
      }
    }
    setIsLoading(false);
  }, []);

  const login = async (email: string, password: string): Promise<{ success: boolean; error?: string }> => {
    try {
      const response = await api.POST('/api/users/login', {
        body: {
          email,
          password,
        },
      });

      if (response.error) {
        return {
          success: false,
          error: (response.error as any)?.error || 'Login failed'
        };
      }

      if (response.data) {
        const data = response.data as unknown as LoginResponse;
        const userData = {
          id: data.user.id,
          name: data.user.name,
          email: data.user.email,
          university: data.user.university,
          university_id: (data.user as any).university_id,
        };
        setUser(userData);
        localStorage.setItem('user', JSON.stringify(userData));
        return { success: true };
      }

      return { success: false, error: 'Login failed' };
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: 'Network error. Please try again.' };
    }
  };

  const signup = async (name: string, email: string, password: string, universityId: string): Promise<{ success: boolean; error?: string }> => {
    try {
      const response = await api.POST('/api/users/', {
        body: {
          name,
          email,
          password,
          university_id: universityId,
        },
      });

      if (response.error) {
        return {
          success: false,
          error: (response.error as any)?.error || 'Signup failed'
        };
      }

      if (response.data) {
        // After successful signup, automatically log the user in
        const userData = {
          id: response.data.id as string,
          name: response.data.name,
          email: response.data.email,
          university: response.data.university || null,
        };
        setUser(userData);
        localStorage.setItem('user', JSON.stringify(userData));
        return { success: true };
      }

      return { success: false, error: 'Signup failed' };
    } catch (error) {
      console.error('Signup error:', error);
      return { success: false, error: 'Network error. Please try again.' };
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };

  const updateUser = async (userId: string, data: { name?: string; password?: string }): Promise<{ success: boolean; error?: string }> => {
    try {
      const response = await api.PUT('/api/users/{user_id}', {
        params: {
          path: {
            user_id: userId,
          },
        },
        body: data,
      });

      if (response.error) {
        return {
          success: false,
          error: (response.error as any)?.error || 'Update failed'
        };
      }

      if (response.data) {
        // Update user in state and localStorage if name was changed
        if (data.name && user) {
          const updatedUser = { ...user, name: response.data.name };
          setUser(updatedUser);
          localStorage.setItem('user', JSON.stringify(updatedUser));
        }
        return { success: true };
      }

      return { success: false, error: 'Update failed' };
    } catch (error) {
      console.error('Update error:', error);
      return { success: false, error: 'Network error. Please try again.' };
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, signup, logout, updateUser, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
