import { Suspense, useState } from "react";
import RichNote from "./Editor/view-create";
import { Button } from "./ui/button";
import { useNavigate } from "@tanstack/react-router";
//import { isAuthenticated } from "@/services/notes.service";
import { useAuth } from "@/hooks/use-auth";
import { triggerAuthChange } from "@/hooks/use-auth"; 
function NotificationBar() {
  const [isCreatingNote, setIsCreatingNote] = useState(false);
  const navigate = useNavigate();
  const authenticated = useAuth(); // Use the custom hook

  const handleCloseForm = () => {
    setIsCreatingNote(false);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user_id");
    triggerAuthChange();
    navigate({ to: "/login" });
  };

  return (
    <>
      <nav className="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <img src="/brain.svg" alt="Brain Icon" className="w-10 h-10" />
              <h1 className="text-xl font-bold text-gray-800 hover:text-gray-600 transition-colors">
                Notty {/* ৻(  •̀ ᗜ •́  ৻) */}
              </h1>
            </div>

            <div className="flex items-center justify-between space-x-6 w-full sm:w-auto">
              {authenticated && (
                <div className="border-l border-gray-200 pl-6 sm:border-0 sm:pl-0">
                  <Button onClick={() => setIsCreatingNote(true)}>
                    Create New Note
                  </Button>
                </div>
              )}

              <div className="flex items-center space-x-4">
                {authenticated ? (
                  <Button variant="destructive" onClick={handleLogout}>
                    Logout
                  </Button>
                ) : (
                  <Button onClick={() => navigate({ to: "/login" })}>
                    Login
                  </Button>
                )}
              </div>
            </div>
          </div>
        </div>
      </nav>

      {isCreatingNote && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-30 z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-2xl">
            <RichNote onClose={handleCloseForm} />
          </div>
        </div>
      )}
    </>
  );
}

// Wrap the component in Suspense
export default function SuspendedNotificationBar() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <NotificationBar />
    </Suspense>
  );
}