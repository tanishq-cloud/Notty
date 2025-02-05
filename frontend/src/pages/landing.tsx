import { useNavigate } from "@tanstack/react-router";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/hooks/use-auth";

export default function LandingPage() {
  const navigate = useNavigate();
 const authenticated = useAuth();
  return (
    <div className="min-h-full flex flex-col justify-center items-center px-4">
   
            

      {/* Hero Section */}
      <section className="flex-1 flex items-center justify-center text-center px-4">
        <div className="max-w-2xl">
          <h2 className="text-4xl font-extrabold text-gray-900 sm:text-5xl">
            Capture Your Thoughts with <span className="text-blue-600">Notty</span>
          </h2>
          <p className="mt-4 text-lg text-gray-600">
            A simple and powerful note-taking app with a rich text editor. Stay organized and never forget an idea again.
          </p>
          <div className="mt-6 space-x-4">
            <Button size="lg" onClick={() => navigate({ to : authenticated ? "/list" : "/register"})}>
              Get Started
            </Button>
            
          </div>
        </div>
      </section>


     
    </div>
  );
}
