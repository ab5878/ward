import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { AlertCircle } from 'lucide-react';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4">
      <div className="w-full max-w-md">
        <div className="bg-card p-8 rounded-lg shadow-[var(--shadow-elev-2)] border border-[hsl(var(--border))]">
          <div className="mb-8 text-center">
            <h1 className="text-3xl font-bold mb-2">Ward v0</h1>
            <p className="text-[hsl(var(--muted-foreground))]">
              Decision Support for Logistics Operations
            </p>
          </div>

          {error && (
            <div
              className="mb-4 p-3 rounded-md bg-[hsl(var(--destructive))]/10 border border-[hsl(var(--destructive))]/20 flex items-center gap-2"
              data-testid="login-error-alert"
            >
              <AlertCircle className="h-4 w-4 text-[hsl(var(--destructive))]" />
              <span className="text-sm text-[hsl(var(--destructive))]">{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium mb-1">
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full px-3 py-2 border border-[hsl(var(--input))] rounded-md focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))] bg-background"
                placeholder="operator@company.com"
                data-testid="login-email-input"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium mb-1">
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={6}
                className="w-full px-3 py-2 border border-[hsl(var(--input))] rounded-md focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))] bg-background"
                placeholder="••••••••"
                data-testid="login-password-input"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] py-2 px-4 rounded-md hover:bg-[hsl(var(--primary))]/90 focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              data-testid="login-submit-button"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-[hsl(var(--muted-foreground))]">
            Don't have an account?{' '}
            <Link
              to="/register"
              className="text-[hsl(var(--primary))] hover:underline"
              data-testid="register-link"
            >
              Register here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
