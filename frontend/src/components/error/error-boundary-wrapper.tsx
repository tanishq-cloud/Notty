// components/ErrorBoundaryWrapper.tsx
import React from 'react';
import { ErrorBoundary } from 'react-error-boundary';
import ErrorSpinner from './error-screen';

interface ErrorBoundaryWrapperProps {
  children: React.ReactNode;
}

const ErrorBoundaryWrapper = ({ children }: ErrorBoundaryWrapperProps) => {
  const handleReset = () => {
    window.location.reload();
  };

  return (
    <ErrorBoundary
      FallbackComponent={ErrorSpinner}
      onReset={handleReset}
      resetKeys={[]}
    >
      {children}
    </ErrorBoundary>
  );
};

export default ErrorBoundaryWrapper;