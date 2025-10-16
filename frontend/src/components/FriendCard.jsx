import { Link } from "react-router";
import { LANGUAGE_TO_FLAG } from "../constants";

const FriendCard = ({ friend }) => {
  return (
    <div className="card bg-base-200 hover:shadow-lg transition-all duration-300 group">
      <div className="card-body p-4 sm:p-5">
        {/* USER INFO */}
        <div className="flex items-center gap-3 mb-4">
          <div className="avatar">
            <div className="w-12 h-12 sm:w-14 sm:h-14 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2 transition-all duration-300 group-hover:ring-secondary">
              <img 
                src={friend.profilePic} 
                alt={friend.fullName}
                className="object-cover"
              />
            </div>
          </div>
          <div>
            <h3 className="font-semibold text-lg truncate">{friend.fullName}</h3>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 mb-4">
          <span className="badge badge-secondary badge-lg gap-1.5">
            {getLanguageFlag(friend.nativeLanguage)}
            <span className="hidden xs:inline">Native:</span> {friend.nativeLanguage}
          </span>
          <span className="badge badge-outline badge-lg gap-1.5">
            {getLanguageFlag(friend.learningLanguage)}
            <span className="hidden xs:inline">Learning:</span> {friend.learningLanguage}
          </span>
        </div>

        <Link 
          to={`/chat/${friend._id}`} 
          className="btn btn-primary w-full mt-auto group-hover:btn-secondary transition-all duration-300"
        >
          Message
        </Link>
      </div>
    </div>
  );
};
export default FriendCard;

export function getLanguageFlag(language) {
  if (!language) return null;

  const langLower = language.toLowerCase();
  const countryCode = LANGUAGE_TO_FLAG[langLower];

  if (countryCode) {
    return (
      <img
        src={`https://flagcdn.com/24x18/${countryCode}.png`}
        alt={`${langLower} flag`}
        className="h-3 mr-1 inline-block"
      />
    );
  }
  return null;
}
