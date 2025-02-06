import { ClimbingBoxLoader } from 'react-spinners';
import { AlertCircle } from 'lucide-react';
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert';

const ErrorSpinner = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
      <Alert variant="destructive" className="mb-8 max-w-md">
        <AlertCircle className="h-4 w-4" />
        <AlertTitle className="text-xl">Oops! Something went wrong 😕</AlertTitle>
        <AlertDescription className="text-lg">
          We're working on fixing this issue! Please try again later 🛠️
        </AlertDescription>
      </Alert>

      <div className="flex flex-col items-center space-y-4">
        <ClimbingBoxLoader color="#000000" size={20} />
        <p className="text-gray-600 mt-4 text-center text-lg">
          Attempting to reconnect... 🔄
        </p>
      </div>

      <div className="mt-8 text-center">
        <p className="text-gray-500">
          Need help? Pray to god.
        </p>
      </div>
    </div>
  );
};

export default ErrorSpinner;