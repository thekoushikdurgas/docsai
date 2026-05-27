"use client";

import { Search } from "lucide-react";
import { useAdminShellSearch } from "@/context/AdminShellSearchContext";

interface AdminSidebarSearchProps {
  collapsed?: boolean;
}

export function AdminSidebarSearch({ collapsed }: AdminSidebarSearchProps) {
  const { openSearch } = useAdminShellSearch();

  return (
    <button
      type="button"
      onClick={openSearch}
      className="c360-sidebar-search-trigger"
      title="Search (Ctrl+K)"
      aria-label="Open search"
    >
      <Search size={15} />
      {!collapsed && (
        <>
          <span className="c360-sidebar-search-trigger__label">
            Search here…
          </span>
          <kbd className="c360-sidebar-search-trigger__kbd">⌘K</kbd>
        </>
      )}
    </button>
  );
}
