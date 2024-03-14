"use client";

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

import Link from "next/link";
import { Button } from "../ui/button";
import { usePathname } from "next/navigation";
import { HamburgerMenuIcon } from "@radix-ui/react-icons";

type NavBarItem = {
  display_name: string | React.ReactNode;
  href: string;
};

const NavBarItem: React.FC<NavBarItem> = ({ display_name, href }) => {
  const pathname = usePathname();

  return (
    <Button
      asChild
      variant="ghost"
      className={`h-8 ${pathname.startsWith(href) && "bg-slate-100"}`}
    >
      <Link href={href}> {display_name}</Link>
    </Button>
  );
};

const ITEMS_NAVBAR: NavBarItem[] = [
  {
    display_name: "Dashboard",
    href: "/dashboard",
  },
  {
    display_name: "Animations",
    href: "/animations",
  },
  {
    display_name: "Colors",
    href: "/colors",
  },
  {
    display_name: "Setup",
    href: "/setup",
  },
];

export const NavBar: React.FC = () => {
  return (
    <>
      <div className="hidden h-20 items-center border-b px-4 sm:flex  md:px-10">
        {ITEMS_NAVBAR.map((item) => (
          <NavBarItem key={item.href} {...item} />
        ))}
      </div>
      <MobileNavbar />
    </>
  );
};

const MobileNavbar: React.FC = () => {
  // left side current page
  // right side hamburger menu
  const pathname = usePathname();

  return (
    <div className="flex h-20 w-full items-center justify-between border-b px-4 sm:hidden">
      <div className="flex-1">
        {ITEMS_NAVBAR.map((item) => (
          <div
            className={`${pathname.startsWith(item.href) ? "flex" : "hidden"}`}
          >
            <NavBarItem key={item.href} {...item} />
          </div>
        ))}
      </div>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button size={"icon"} variant="outline">
            <HamburgerMenuIcon className="h-4 w-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="w-56">
          <DropdownMenuGroup>
            {ITEMS_NAVBAR.map((item) => (
              <Link href={item.href}>
                <DropdownMenuItem key={item.href}>
                  {item.display_name}
                </DropdownMenuItem>
              </Link>
            ))}
          </DropdownMenuGroup>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
};
