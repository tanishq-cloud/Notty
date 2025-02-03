import { createRootRoute, Outlet } from "@tanstack/react-router";
import NotificationBar from "@/components/notification-bar";
import Footer from "@/components/footer";

export const Route = createRootRoute({
  component: () => {
    return (
      <div className="flex flex-col min-h-screen bg-gray-50">
        {/* Sticky Notification Bar */}
        <NotificationBar />

        {/* Main Content */}
        <main className="flex-1 container mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <Outlet />
        </main>

        {/* Footer */}
        <Footer />
      </div>
    );
  },
});

export default Route;
