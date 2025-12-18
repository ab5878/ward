import React, { useEffect, useState } from 'react';

/**
 * Mobile Optimizations Component
 * Adds mobile-specific optimizations and utilities
 */

// Hook to detect mobile device
export function useIsMobile() {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768); // md breakpoint
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  return isMobile;
}

// Hook to prevent zoom on input focus (iOS)
export function usePreventZoom() {
  useEffect(() => {
    const meta = document.querySelector('meta[name="viewport"]');
    if (meta) {
      const originalContent = meta.getAttribute('content');
      meta.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
      
      return () => {
        if (originalContent) {
          meta.setAttribute('content', originalContent);
        }
      };
    }
  }, []);
}

// Component to add mobile-specific styles
export function MobileOptimizations() {
  usePreventZoom();
  
  return null; // This component doesn't render anything
}

// Utility to ensure touch targets are at least 44px
export const MIN_TOUCH_TARGET = 44;

export function ensureTouchTarget(element) {
  if (element) {
    const rect = element.getBoundingClientRect();
    const minSize = MIN_TOUCH_TARGET;
    
    if (rect.width < minSize || rect.height < minSize) {
      const padding = Math.max(
        (minSize - rect.width) / 2,
        (minSize - rect.height) / 2,
        0
      );
      element.style.padding = `${padding}px`;
    }
  }
}

