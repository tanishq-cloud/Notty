import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.tsx';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { Suspense } from 'react';
import LoadingScreen from './components/loading-screen.tsx';
import ErrorBoundaryWrapper from './components/error/error-boundary-wrapper.tsx';

const queryClient = new QueryClient();

createRoot(document.getElementById('root')!).render(
  <QueryClientProvider client={queryClient}>
    <ErrorBoundaryWrapper>
      <Suspense fallback={<LoadingScreen />}>
        <App />
      </Suspense>
    </ErrorBoundaryWrapper>
    <ReactQueryDevtools initialIsOpen={false} />
  </QueryClientProvider>
);