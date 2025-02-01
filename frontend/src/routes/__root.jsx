import { createRootRoute, Link, Outlet } from "@tanstack/react-router";



export const Route = createRootRoute({
  component: () => {
    

    return (
        
      <>
      {/* 🛠 */}
        <div className="p-2 flex justify-center items-center gap-4 w-full">
          <div className="flex space-x-4 border-b border-gray-300 w-full justify-center">
            
            <Link href="/login">Click here for login</Link>
          </div>
          

        </div>
        <Link href="list">List the notes! </Link>
        <hr className="my-4" />

        <Outlet />

      </>
    );
  },
});
