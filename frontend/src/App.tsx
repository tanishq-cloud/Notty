import NotificationBar from "./components/notification-bar";
import { RouterProvider, createRouter } from "@tanstack/react-router";
import { routeTree } from "./routeTree.gen";
import Footer from "./components/footer";


const router = createRouter({ routeTree });

function App() {


  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      {/* Navigation Bar 🔨*/}
      <NotificationBar />

      {/* Main tab content (¬⤙¬ ) */}
      <main className="flex-grow container mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="w-full">
          <div className="tabs-content">
            <RouterProvider router={router} />
          </div>
        </div>
      </main>

      {/* Footer 🦉*/}
      <Footer />
    </div>
  );
}

export default App;
