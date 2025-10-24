import { Link, useLocation } from "react-router-dom";
import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
} from "@/components/ui/navigation-menu";
import { Button } from "@/components/ui/button";

export default function Navbar() {
  const location = useLocation();

  const navItems = [
    { name: "Home", path: "/" },
    { name: "Forum", path: "/forum" },
    { name: "Profile", path: "/profile" },
  ];

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

      {/* Right: Login Button */}
      <Link to="/login">
        <Button
          variant="secondary"
          className="bg-[#FBF8BE] text-[#234E70] hover:bg-[#f1edaa]"
        >
          Login
        </Button>
      </Link>
    </header>
  );
}
