function NotificationBar(){
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
                     
        
                      <div className="border-l border-gray-200 pl-6 sm:border-0 sm:pl-0">
                      
                      </div>
                    </div>
                  </div>
                </div>
              </nav>
            </>
    )
}

export default NotificationBar;