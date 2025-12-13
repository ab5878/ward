import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for token on mount
    const token = localStorage.getItem('token');
    if (token) {
      api.setAuthToken(token);
      // Verify token
      api.get('/auth/me')
        .then(response => {
          setUser(response.data);
        })
        .catch(() => {
          localStorage.removeItem('token');
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email, password) => {
    const response = await api.post('/auth/login', { email, password });
    const { access_token } = response.data;
    localStorage.setItem('token', access_token);
    api.setAuthToken(access_token);
    
    const userResponse = await api.get('/auth/me');
    setUser(userResponse.data);
    
    return userResponse.data;
  };

  const register = async (email, password) => {
    const response = await api.post('/auth/register', { email, password });
    const { access_token } = response.data;
    localStorage.setItem('token', access_token);
    api.setAuthToken(access_token);
    
    const userResponse = await api.get('/auth/me');
    setUser(userResponse.data);
    
    return userResponse.data;
  };

  const logout = () => {
    localStorage.removeItem('token');
    api.setAuthToken(null);
    setUser(null);
  };

  const value = {
    user,
    login,
    register,
    logout,
    loading
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
