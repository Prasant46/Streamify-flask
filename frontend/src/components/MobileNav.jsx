import { Link } from "react-router";
import { HomeIcon, UsersIcon, BellIcon, XIcon, LogOutIcon } from "lucide-react";
import useAuthUser from "../hooks/useAuthUser";
import useLogout from "../hooks/useLogout";

const MobileNav = ({ isOpen, onClose }) => {
  const { authUser } = useAuthUser();
  const { logoutMutation } = useLogout();

  if (!isOpen) return null;

  const handleLogout = () => {
    onClose();
    logoutMutation();
  };

  return (
    <div className="lg:hidden fixed inset-0 z-50">
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-black bg-opacity-50 transition-opacity" 
        onClick={onClose}
      />
      
      {/* Drawer */}
      <div className="fixed inset-y-0 left-0 w-64 bg-base-200 shadow-xl transform transition-transform">
        <div className="p-4 border-b border-base-300 flex justify-between items-center">
          <span className="text-xl font-bold">Menu</span>
          <button className="btn btn-ghost btn-circle" onClick={onClose}>
            <XIcon className="h-6 w-6" />
          </button>
        </div>

        <nav className="flex-1 p-4 space-y-2">
          <Link
            to="/"
            className="btn btn-ghost justify-start w-full gap-3"
            onClick={onClose}
          >
            <HomeIcon className="h-5 w-5" />
            Home
          </Link>
          
          <Link
            to="/friends"
            className="btn btn-ghost justify-start w-full gap-3"
            onClick={onClose}
          >
            <UsersIcon className="h-5 w-5" />
            Friends
          </Link>
          
          <Link
            to="/notifications"
            className="btn btn-ghost justify-start w-full gap-3"
            onClick={onClose}
          >
            <BellIcon className="h-5 w-5" />
            Notifications
          </Link>
        </nav>

        {/* User Profile and Logout */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-base-300 bg-base-200">
          <div className="flex items-center gap-3 mb-4">
            <div className="avatar">
              <div className="w-10 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2">
                <img 
                  src={authUser?.profilePic} 
                  alt={authUser?.fullName}
                  className="w-full h-full object-cover" 
                />
              </div>
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-semibold text-sm truncate">{authUser?.fullName}</p>
              <p className="text-xs text-success flex items-center gap-1">
                <span className="size-2 rounded-full bg-success inline-block" />
                Online
              </p>
            </div>
          </div>
          
          {/* Logout button */}
          <button 
            onClick={handleLogout}
            className="btn btn-error btn-outline w-full flex items-center justify-center gap-2 hover:bg-error hover:text-white"
          >
            <LogOutIcon className="h-5 w-5" />
            Logout
          </button>
        </div>
      </div>
    </div>
  );
};

export default MobileNav;
