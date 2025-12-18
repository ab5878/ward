import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, Plus, Mic, BarChart3, User } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function MobileBottomNav() {
  const location = useLocation();
  
  const navItems = [
    { path: '/dashboard', icon: Home, label: 'Dashboard' },
    { path: '/cases/new', icon: Plus, label: 'New Case' },
    { path: '/cases/voice', icon: Mic, label: 'Voice' },
    { path: '/dashboard/analytics', icon: BarChart3, label: 'Analytics' },
    { path: '/settings/developer', icon: User, label: 'Settings' },
  ];

  const isActive = (path) => {
    if (path === '/dashboard') {
      return location.pathname === '/dashboard' || location.pathname.startsWith('/cases/');
    }
    return location.pathname === path || location.pathname.startsWith(path);
  };

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-gray-200 md:hidden">
      <div className="flex justify-around items-center h-16 px-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.path);
          return (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                "flex flex-col items-center justify-center flex-1 h-full transition-colors",
                active
                  ? "text-blue-600"
                  : "text-gray-500 hover:text-gray-700"
              )}
            >
              <Icon className={cn("h-6 w-6 mb-1", active && "text-blue-600")} />
              <span className={cn("text-xs font-medium", active && "text-blue-600")}>
                {item.label}
              </span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}

