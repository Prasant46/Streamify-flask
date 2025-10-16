import { useQuery } from "@tanstack/react-query";
import { getUserFriends } from "../lib/api";
import { Link } from "react-router";
import { UsersIcon } from "lucide-react";

import FriendCard from "../components/FriendCard";
import NoFriendsFound from "../components/NoFriendsFound";

const FriendsPage = () => {
  const { data: friends = [], isLoading: loadingFriends } = useQuery({
    queryKey: ["friends"],
    queryFn: getUserFriends,
  });

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-base-100 p-4">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-4 bg-base-200 rounded-lg shadow-sm">
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight">Your Friends</h2>
          <Link 
            to="/notifications" 
            className="btn btn-primary btn-sm sm:btn-md w-full sm:w-auto"
          >
            <UsersIcon className="mr-2 size-4" />
            Friend Requests
          </Link>
        </div>

        {/* Content */}
        <div className="p-4">
          {loadingFriends ? (
            <div className="flex justify-center items-center min-h-[300px]">
              <span className="loading loading-spinner loading-lg text-primary" />
            </div>
          ) : friends.length === 0 ? (
            <div className="max-w-md mx-auto">
              <NoFriendsFound />
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 gap-4 sm:gap-6">
              {friends.map((friend) => (
                <FriendCard key={friend._id} friend={friend} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FriendsPage;
