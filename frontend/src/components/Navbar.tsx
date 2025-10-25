import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import universeLogo from "@/assets/universe.svg";

export default function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const navItems = [
    { name: "Home", path: "/" },
    { name: "Explore", path: "/explore" },
  ];

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="sticky top-0 z-40 w-full">
      <div className="relative">
        {/* Glass Background */}
        <nav className="w-full bg-gradient-to-r from-[#234E70]/95 via-[#1f6b8a]/95 to-[#0ea5a4]/95 backdrop-blur-md border-b border-white/10 shadow-lg">
          <div className="max-w-7xl mx-auto px-4 sm:px-6">
            <div className="grid grid-cols-[220px_1fr_220px] items-center h-16">
              {/* Left: Logo */}
              <Link to="/" className="flex items-center gap-3">
                <Avatar className="w-8 h-8">
                  <AvatarImage src={universeLogo} alt="UniVerse" />
                </Avatar>
                <span className="text-xl font-semibold tracking-wide text-white">UniVerse</span>
              </Link>

              {/* Center: Nav Menu */}
              <div className="hidden md:flex items-center justify-center">
                <div className="inline-flex items-center gap-1 rounded-full py-1 px-2">
                  {navItems.map((item) => (
                    <Link
                      key={item.path}
                      to={item.path}
                      className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${
                        location.pathname === item.path
                          ? "bg-white/20 text-white shadow-sm"
                          : "text-white/90 hover:bg-white/10 hover:text-white"
                      }`}
                    >
                      {item.name}
                    </Link>
                  ))}
                </div>
              </div>

              {/* Right: User Info or Login/Signup */}
              <div className="flex items-center justify-end gap-3">
                {user ? (
                  <>
                    <button
                      onClick={() => navigate('/profile')}
                      className="hover:cursor-pointer flex items-center gap-2 bg-white/10 px-3 py-1 rounded-full hover:bg-white/20 transition"
                    >
                      <Avatar className="h-7 w-7">
                        <AvatarFallback className="bg-[#FBF8BE] text-[#234E70] text-sm">
                          {getInitials(user.name)}
                        </AvatarFallback>
                      </Avatar>
                      <span className="text-sm font-medium text-white hidden sm:inline">
                        {user.name}
                      </span>
                    </button>
                    <Button
                      onClick={handleLogout}
                      variant="ghost"
                      className="text-white/90 hover:text-white hover:bg-white/10"
                      size="sm"
                    >
                      Logout
                    </Button>
                  </>
                ) : (
                  <div className="flex items-center gap-2">
                    <Link to="/login">
                      <Button
                        variant="ghost"
                        className="text-white/90 hover:text-white hover:bg-white/10"
                        size="sm"
                      >
                        Login
                      </Button>
                    </Link>
                    <Link to="/signup">
                      <Button
                        variant="default"
                        className="bg-[#FBF8BE] text-[#234E70] hover:bg-[#f1edaa] shadow-sm"
                        size="sm"
                      >
                        Sign Up
                      </Button>
                    </Link>
                  </div>
                )}
              </div>
            </div>
          </div>
        </nav>
      </div>
    </header>
  );
}
