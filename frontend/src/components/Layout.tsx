import { Link, Outlet, useNavigate } from "react-router";
import { cn } from "@/lib/utils";
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import { FileText } from "lucide-react";

export function Layout() {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen">
      <div className="border-b bg-white/75 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-4">
          <NavigationMenu className="h-16">
            <NavigationMenuList className="w-full flex justify-between">
              <div className="flex items-center gap-8">
                <NavigationMenuItem>
                  <NavigationMenuLink
                    className={cn(navigationMenuTriggerStyle(), "font-semibold")}
                    href="/"
                    onClick={(e) => {
                      e.preventDefault();
                      navigate('/');
                    }}
                  >
                    <FileText className="w-5 h-5 mr-2" />
                    Repo Digest Tool
                  </NavigationMenuLink>
                </NavigationMenuItem>
              </div>
            </NavigationMenuList>
          </NavigationMenu>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 py-8">
        <Outlet />
      </div>
    </div>
  );
}
