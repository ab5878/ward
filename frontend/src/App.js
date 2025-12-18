import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Register from './pages/Register';
import Contact from './pages/Contact';
import HowItWorks from './pages/HowItWorks';
import WhyWard from './pages/WhyWard';
import CaseDetail from './pages/CaseDetail';
import VoiceCase from './pages/VoiceCase';
import AnalyticsDashboard from './pages/Analytics';
import DeveloperSettings from './pages/Developer';
import AlignmentCheck from './pages/AlignmentCheck';
import OperatorOnboarding from './pages/OperatorOnboarding';
import OperatorDashboard from './pages/OperatorDashboard';
import OperatorSettings from './pages/OperatorSettings';
import FleetManagement from './pages/FleetManagement';
import DriverApp from './pages/DriverApp';
import { Toaster } from "@/components/ui/sonner"
import { MobileOptimizations } from './components/MobileOptimizations';

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
        <MobileOptimizations />
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/how-it-works" element={<HowItWorks />} />
          <Route path="/why-ward" element={<WhyWard />} />
          <Route path="/internal/alignment" element={<AlignmentCheck />} />
          <Route 
            path="/operator/onboard" 
            element={
              <ProtectedRoute>
                <OperatorOnboarding />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/operator/dashboard" 
            element={
              <ProtectedRoute>
                <OperatorDashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/operator/settings" 
            element={
              <ProtectedRoute>
                <OperatorSettings />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/operator/fleet" 
            element={
              <ProtectedRoute>
                <FleetManagement />
              </ProtectedRoute>
            } 
          />
          <Route path="/driver/:token" element={<DriverApp />} />
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
