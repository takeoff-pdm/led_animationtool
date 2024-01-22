"use client";

import Link from "next/link";
import { Button } from "../ui/button";
import { usePathname } from "next/navigation";

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
    href: "/about",
  },
  {
    display_name: "Setup",
    href: "/setup",
  },
];

export const NavBar: React.FC = () => {
  return (
    <div className="h-20 flex items-center px-10 border-b">
      {ITEMS_NAVBAR.map((item) => (
        <NavBarItem key={item.href} {...item} />
      ))}
    </div>
  );
};
