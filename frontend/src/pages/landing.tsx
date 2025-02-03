import { useNavigate } from "@tanstack/react-router";
import { Button } from "@/components/ui/button";

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
   
            

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
            <Button size="lg" onClick={() => navigate({ to: "/register" })}>
              Get Started
            </Button>
            
          </div>
        </div>
      </section>


     
    </div>
  );
}
