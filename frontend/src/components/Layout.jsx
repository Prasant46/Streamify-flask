import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

const Layout = ({ children, showSidebar = false }) => {
  return (
    <div className="min-h-screen">
      <div className="flex h-screen overflow-hidden">
        {/* Sidebar - hidden on mobile, visible on lg screens */}
        {showSidebar && <Sidebar />}
        
        {/* Main content area */}
        <div className="flex-1 flex flex-col w-full">
          <Navbar />
          {/* main content - scrollable container */}
          <main className="flex-1 overflow-y-auto bg-base-100">
            <div className="container mx-auto">{children}</div>
          </main>
        </div>
      </div>
    </div>
  );
};
export default Layout;
