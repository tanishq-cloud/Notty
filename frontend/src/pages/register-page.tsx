import { useState } from 'react';
import { useNavigate } from "@tanstack/react-router";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { register } from '@/services/notes.service';

export default function RegisterPage() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    const formData = new FormData(e.currentTarget);
    const credentials = {
      full_name: formData.get('full_name') as string,
      username: formData.get('username') as string,
      password: formData.get('password') as string,
    };

    try {
      await register(credentials);
      setSuccess(true);
      // Delay navigation to login page
      setTimeout(() => {
        navigate({ to: '/login' });
      }, 2000);
    } catch (err) {
      setError('Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-md space-y-8 p-6">
        <div className="text-center">
          <h1 className="text-2xl font-bold">Create an account</h1>
        </div>
        
        {success ? (
          <div className="bg-green-50 p-4 rounded-md text-center">
            <p className="text-green-800 font-medium">Registration successful!</p>
            <p className="text-green-600 text-sm mt-1">Redirecting to login page...</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="text-red-500 text-sm text-center">
                {error}
              </div>
            )}
            
            <div className="space-y-2">
              <Input
                name="full_name"
                type="text"
                required
                placeholder="Username"
              />
            </div>

            <div className="space-y-2">
              <Input
                name="username"
                type="text"
                required
                placeholder="Email address"
              />
            </div>

            <div className="space-y-2">
              <Input
                name="password"
                type="password"
                required
                placeholder="Password"
                minLength={6}
              />
            </div>

            <Button
              type="submit"
              className="w-full"
              disabled={isLoading}
            >
              {isLoading ? 'Creating account...' : 'Create account'}
            </Button>

            <div className="text-center text-sm">
              <span className="text-gray-500">Already have an account? </span>
              <Button 
                variant="link" 
                className="p-0 h-auto font-semibold"
                onClick={() => navigate({ to: '/login' })}
              >
                Sign in
              </Button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}