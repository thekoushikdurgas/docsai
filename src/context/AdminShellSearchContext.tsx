"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { AdminNavCommandPalette } from "@/components/shared/AdminNavCommandPalette";

interface AdminShellSearchContextValue {
  openSearch: () => void;
  closeSearch: () => void;
  searchOpen: boolean;
}

const AdminShellSearchContext =
  createContext<AdminShellSearchContextValue | null>(null);

export function AdminShellSearchProvider({ children }: { children: ReactNode }) {
  const [searchOpen, setSearchOpen] = useState(false);

  const openSearch = useCallback(() => setSearchOpen(true), []);
  const closeSearch = useCallback(() => setSearchOpen(false), []);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setSearchOpen((o) => !o);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  const value = useMemo(
    () => ({
      openSearch,
      closeSearch,
      searchOpen,
    }),
    [openSearch, closeSearch, searchOpen],
  );

  return (
    <AdminShellSearchContext.Provider value={value}>
      {children}
      <AdminNavCommandPalette open={searchOpen} onClose={closeSearch} />
    </AdminShellSearchContext.Provider>
  );
}

export function useAdminShellSearch(): AdminShellSearchContextValue {
  const ctx = useContext(AdminShellSearchContext);
  if (!ctx) {
    throw new Error(
      "useAdminShellSearch must be used within AdminShellSearchProvider",
    );
  }
  return ctx;
}
