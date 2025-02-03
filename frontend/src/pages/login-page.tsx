import { useState } from 'react';
import { useNavigate } from "@tanstack/react-router";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { login } from '@/services/notes.service';
import { toast } from 'react-toastify';
import { triggerAuthChange } from '@/hooks/use-auth';

function LoginPage() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    const formData = new FormData(e.currentTarget);

    try {
     const d = await login({
        username: formData.get('username') as string,
        password: formData.get('password') as string,
      });
      console.log(JSON.stringify(d))
      toast.success("Login successfull!")   
      triggerAuthChange();
      navigate({ to: '/list' });
    } catch (err) {
      setError('Invalid username or password');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-md space-y-8 p-6">
        <div className="text-center">
          <h1 className="text-2xl font-bold">Sign in to your account</h1>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="text-red-500 text-sm text-center">
              {error}
            </div>
          )}
          
          <div>
            <Input
              name="username"
              type="text"
              required
              placeholder="Username"
            />
          </div>

          <div>
            <Input
              name="password"
              type="password"
              required
              placeholder="Password"
            />
          </div>

          <Button
            type="submit"
            className="w-full"
            disabled={isLoading}
          >
            {isLoading ? 'Signing in...' : 'Sign in'}
          </Button>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;
