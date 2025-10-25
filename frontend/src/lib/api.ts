const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

async function apiFetch<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        error: `HTTP ${response.status}: ${response.statusText}`,
      }));
      throw new Error(error.error || "An error occurred");
    }

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}

// Types

export interface University {
  id: string;
  name: string;
  user_count?: number;
  class_count?: number;
}

export interface User {
  id: string;
  name: string;
  email: string;
  created_at: string;
  university_id?: string;
}

export interface Class {
  id: string;
  name: string;
  university_id: string;
  tags?: Tag[];
  discussion_count?: number;
}

export interface Tag {
  id: string;
  name: string;
}

export interface Discussion {
  id: string;
  title: string;
  body: string;
  created_at: string;
  author: string;
  university: string;
  class: string;
  reply_count: number;
}

export interface Reply {
  id: string;
  body: string;
  created_at: string;
  author: string;
  author_id: string;
  discussion_id: string;
  discussion_title?: string;
}

// University

export const universityApi = {
  getAll: (search?: string) => {
    const params = search ? `?q=${encodeURIComponent(search)}` : "";
    return apiFetch<University[]>(`/universities${params}`);
  },

  getById: (id: string) => {
    return apiFetch<University>(`/universities/${id}`);
  },

  getClasses: (id: string) => {
    return apiFetch<Class[]>(`/universities/${id}/classes`);
  },

  getUsers: (id: string) => {
    return apiFetch<User[]>(`/universities/${id}/users`);
  },

  getStats: (id: string) => {
    return apiFetch<{
      id: string;
      name: string;
      user_count: number;
      class_count: number;
      total_discussions: number;
    }>(`/universities/${id}/stats`);
  },

  create: (name: string) => {
    return apiFetch<University>("/universities", {
      method: "POST",
      body: JSON.stringify({ name }),
    });
  },

  update: (id: string, name: string) => {
    return apiFetch<University>(`/universities/${id}`, {
      method: "PUT",
      body: JSON.stringify({ name }),
    });
  },

  delete: (id: string) => {
    return apiFetch<{ message: string }>(`/universities/${id}`, {
      method: "DELETE",
    });
  },
};

// Reply
export const replyApi = {
  getAll: (params?: { discussion_id?: string; user_id?: string }) => {
    const queryParams = new URLSearchParams();
    if (params?.discussion_id)
      queryParams.append("discussion_id", params.discussion_id);
    if (params?.user_id) queryParams.append("user_id", params.user_id);

    const query = queryParams.toString();
    return apiFetch<Reply[]>(`/replies${query ? `?${query}` : ""}`);
  },

  getById: (id: string) => {
    return apiFetch<Reply>(`/replies/${id}`);
  },

  create: (data: { body: string; user_id: string; discussion_id: string }) => {
    return apiFetch<Reply>("/replies", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  update: (id: string, body: string) => {
    return apiFetch<Reply>(`/replies/${id}`, {
      method: "PUT",
      body: JSON.stringify({ body }),
    });
  },

  delete: (id: string) => {
    return apiFetch<{ message: string }>(`/replies/${id}`, {
      method: "DELETE",
    });
  },
};

export const api = {
  universities: universityApi,
  replies: replyApi,
};

export default api;

