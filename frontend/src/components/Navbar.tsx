import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
} from "@/components/ui/navigation-menu";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

export default function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const navItems = [
    { name: "Home", path: "/" },
    { name: "Explore", path: "/explore" },
    { name: "Profile", path: "/profile" },
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
    <header className="flex justify-between items-center px-8 py-4 bg-[#234E70] text-white shadow-md">
      {/* Left: Logo */}
      <Link to="/" className="text-2xl font-bold tracking-wide">
        UniVerse
      </Link>

      {/* Center: Nav Menu */}
      <NavigationMenu>
        <NavigationMenuList className="flex gap-6">
          {navItems.map((item) => (
            <NavigationMenuItem key={item.path}>
              <NavigationMenuLink asChild>
                <Link
                  to={item.path}
                  className={`text-white hover:text-[#FBF8BE] transition ${
                    location.pathname === item.path
                      ? "underline underline-offset-4 decoration-[#FBF8BE]"
                      : ""
                  }`}
                >
                  {item.name}
                </Link>
              </NavigationMenuLink>
            </NavigationMenuItem>
          ))}
        </NavigationMenuList>
      </NavigationMenu>

      {/* Right: User Info or Login Button */}
      {user ? (
        <div className="flex items-center gap-3">
          <Avatar className="h-8 w-8">
            <AvatarFallback className="bg-[#FBF8BE] text-[#234E70] text-sm">
              {getInitials(user.name)}
            </AvatarFallback>
          </Avatar>
          <span className="text-sm font-medium">{user.name}</span>
          <Button
            onClick={handleLogout}
            variant="ghost"
            className="text-white hover:text-[#FBF8BE] hover:bg-transparent"
            size="sm"
          >
            Logout
          </Button>
        </div>
      ) : (
        <Link to="/login">
          <Button
            variant="secondary"
            className="bg-[#FBF8BE] text-[#234E70] hover:bg-[#f1edaa]"
          >
            Login
          </Button>
        </Link>
      )}
    </header>
  );
}
