"use client";

import { createContext, useContext, type ReactNode } from "react";

export interface DataFiltersPeekValue {
  pinned: boolean;
  togglePinned: () => void;
  notifyFilterOverlayOpen: (open: boolean) => void;
}

const DataFiltersPeekContext = createContext<DataFiltersPeekValue | null>(null);

export function useDataFiltersPeek(): DataFiltersPeekValue | null {
  return useContext(DataFiltersPeekContext);
}

export function DataFiltersPeekProvider({
  children,
  value,
}: {
  children: ReactNode;
  value: DataFiltersPeekValue;
}) {
  return (
    <DataFiltersPeekContext.Provider value={value}>
      {children}
    </DataFiltersPeekContext.Provider>
  );
}
