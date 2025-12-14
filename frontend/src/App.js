import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Register from './pages/Register';
import CaseDetail from './pages/CaseDetail';
import VoiceCase from './pages/VoiceCase';
import AnalyticsDashboard from './pages/Analytics';
import DeveloperSettings from './pages/Developer';
import { Toaster } from "@/components/ui/sonner"

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return <div>Loading...</div>;
  }
  
  if (!user) {
    return <Navigate to="/login" />;
  }
  
  return children;
};

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/dashboard/analytics" 
            element={
              <ProtectedRoute>
                <AnalyticsDashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/settings/developer" 
            element={
              <ProtectedRoute>
                <DeveloperSettings />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/cases/new" 
            element={
              <ProtectedRoute>
                <VoiceCase mode="text" />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/cases/voice" 
            element={
              <ProtectedRoute>
                <VoiceCase mode="voice" />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/cases/:caseId" 
            element={
              <ProtectedRoute>
                <CaseDetail />
              </ProtectedRoute>
            } 
          />
        </Routes>
        <Toaster />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
