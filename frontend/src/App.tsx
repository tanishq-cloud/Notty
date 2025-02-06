
import { RouterProvider, createRouter } from "@tanstack/react-router";
import { routeTree } from "./routeTree.gen";
import { Suspense } from "react";
import LoadingScreen from "./components/loading-screen";
import {ToastContainer} from 'react-toastify';

const router = createRouter({ routeTree });

function App() {


  return (
    <div >
      <Suspense fallback={<LoadingScreen />} >
      <RouterProvider router={router} />
      </Suspense>
            
      
      <ToastContainer 
        position="top-right"
        autoClose={1000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
    </div>
  );
}

export default App;
