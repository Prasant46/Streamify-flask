import { Link, useLocation } from "react-router";
import useAuthUser from "../hooks/useAuthUser";
import { BellIcon, LogOutIcon, MenuIcon, ShipWheelIcon } from "lucide-react";
import ThemeSelector from "./ThemeSelector";
import useLogout from "../hooks/useLogout";
import { useState } from "react";
import MobileNav from "./MobileNav";

const Navbar = () => {
  const { authUser } = useAuthUser();
  const location = useLocation();
  const isChatPage = location.pathname?.startsWith("/chat");
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const { logoutMutation } = useLogout();

  return (
    <>
      <nav className="bg-base-200 border-b border-base-300 sticky top-0 z-30 h-16 flex items-center">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between w-full">
            <div className="flex items-center">
              {/* Mobile menu button */}
              <button 
                className="lg:hidden btn btn-ghost btn-circle mr-2"
                onClick={() => setIsMobileMenuOpen(true)}
              >
                <MenuIcon className="h-6 w-6" />
              </button>

              {/* Logo - show on chat page or desktop */}
              {(isChatPage || !location.pathname.startsWith("/chat")) && (
                <Link to="/" className="flex items-center gap-2">
                  <ShipWheelIcon className="size-8 text-primary" />
                  <span className="text-xl sm:text-2xl font-bold font-mono bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary">
                    Streamify
                  </span>
                </Link>
              )}
            </div>

            {/* Right side items */}
            <div className="flex items-center gap-2 sm:gap-4">
              <Link to="/notifications" className="btn btn-ghost btn-circle">
                <BellIcon className="h-6 w-6 text-base-content opacity-70" />
              </Link>

              <ThemeSelector />

              <div className="avatar">
                <div className="w-9 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2">
                  <img src={authUser?.profilePic} alt="User Avatar" />
                </div>
              </div>

              {/* Logout button - hidden on mobile, visible on lg screens */}
              <button 
                className="hidden lg:flex btn btn-ghost btn-circle" 
                onClick={logoutMutation}
                aria-label="Logout"
              >
                <LogOutIcon className="h-6 w-6 text-base-content opacity-70" />
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Mobile Navigation */}
      <MobileNav 
        isOpen={isMobileMenuOpen} 
        onClose={() => setIsMobileMenuOpen(false)} 
      />
    </>
  );
};
export default Navbar;
