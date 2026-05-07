https://21st.dev/community/components/ruixenui/floating-nav/default
You are given a task to integrate an existing React component in the codebase

The codebase should support:
- shadcn project structure  
- Tailwind CSS
- Typescript

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind or Typescript.

Determine the default path for components and styles. 
If default path for components is not /components/ui, provide instructions on why it's important to create this folder
Copy-paste this component to /components/ui folder:
```tsx
floating-nav.tsx
"use client";

import React, { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { Home, Search, Bell, User, Settings, Bookmark } from "lucide-react";

const FloatingNav = () => {
  const [active, setActive] = useState(0);
  const [indicatorStyle, setIndicatorStyle] = useState({ width: 0, left: 0 });
  const containerRef = useRef<HTMLDivElement>(null);
  const btnRefs = useRef<(HTMLButtonElement | null)[]>([]);

  const items = [
    { id: 0, icon: <Home size={22} />, label: "Home" },
    { id: 1, icon: <Search size={22} />, label: "Search" },
    { id: 2, icon: <Bell size={22} />, label: "Alerts" },
    { id: 3, icon: <User size={22} />, label: "Profile" },
    { id: 4, icon: <Bookmark size={22} />, label: "Saved" },
    { id: 5, icon: <User size={22} />, label: "Profile" },
    { id: 6, icon: <Settings size={22} />, label: "Settings" },
  ];

  // Update indicator position when active changes or resize
  useEffect(() => {
    const updateIndicator = () => {
      if (btnRefs.current[active] && containerRef.current) {
        const btn = btnRefs.current[active];
        const container = containerRef.current;
        if (!btn) return;
        const btnRect = btn.getBoundingClientRect();
        const containerRect = container.getBoundingClientRect();

        setIndicatorStyle({
          width: btnRect.width,
          left: btnRect.left - containerRect.left,
        });
      }
    };

    updateIndicator();
    window.addEventListener("resize", updateIndicator);
    return () => window.removeEventListener("resize", updateIndicator);
  }, [active]);

  return (
    <div className="fixed bottom-4 left-1/2 -translate-x-1/2 z-50 w-full max-w-lg px-2 mb-64">
      <div
        ref={containerRef}
        className="relative flex items-center justify-between bg-white dark:bg-neutral-900 shadow-xl rounded-full px-1 py-2 border border-gray-200 dark:border-gray-800"
      >
        {items.map((item, index) => (
          <button
            key={item.id}
            ref={(el) => (btnRefs.current[index] = el)}
            onClick={() => setActive(index)}
            className="relative flex flex-col items-center justify-center flex-1 px-2 py-2 text-sm font-medium text-gray-600 dark:text-gray-300"
          >
            <div className="z-10">{item.icon}</div>
            {/* hide labels on small screens */}
            <span className="text-xs mt-1 hidden sm:block">{item.label}</span>
          </button>
        ))}

        {/* Sliding Active Indicator */}
        <motion.div
          animate={indicatorStyle}
          transition={{ type: "spring", stiffness: 400, damping: 30 }}
          className="absolute top-1 bottom-1 rounded-full bg-blue-500/10 dark:bg-blue-400/20"
        />
      </div>
    </div>
  );
};

export default FloatingNav;


demo.tsx
import FloatingNav from "@/components/ui/floating-nav";

export default function DemoOne() {
  return <FloatingNav />;
}

```

Install NPM dependencies:
```bash
lucide-react, framer-motion
```

Implementation Guidelines
 1. Analyze the component structure and identify all required dependencies
 2. Review the component's argumens and state
 3. Identify any required context providers or hooks and install them
 4. Questions to Ask
 - What data/props will be passed to this component?
 - Are there any specific state management requirements?
 - Are there any required assets (images, icons, etc.)?
 - What is the expected responsive behavior?
 - What is the best place to use this component in the app?

Steps to integrate
 0. Copy paste all the code above in the correct directories
 1. Install external dependencies
 2. Fill image assets with Unsplash stock images you know exist
 3. Use lucide-react icons for svgs or logos if component requires them
"use client";

import React, { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { Home, Search, Bell, User, Settings, Bookmark } from "lucide-react";

const FloatingNav = () => {
  const [active, setActive] = useState(0);
  const [indicatorStyle, setIndicatorStyle] = useState({ width: 0, left: 0 });
  const containerRef = useRef<HTMLDivElement>(null);
  const btnRefs = useRef<(HTMLButtonElement | null)[]>([]);

  const items = [
    { id: 0, icon: <Home size={22} />, label: "Home" },
    { id: 1, icon: <Search size={22} />, label: "Search" },
    { id: 2, icon: <Bell size={22} />, label: "Alerts" },
    { id: 3, icon: <User size={22} />, label: "Profile" },
    { id: 4, icon: <Bookmark size={22} />, label: "Saved" },
    { id: 5, icon: <User size={22} />, label: "Profile" },
    { id: 6, icon: <Settings size={22} />, label: "Settings" },
  ];

  // Update indicator position when active changes or resize
  useEffect(() => {
    const updateIndicator = () => {
      if (btnRefs.current[active] && containerRef.current) {
        const btn = btnRefs.current[active];
        const container = containerRef.current;
        if (!btn) return;
        const btnRect = btn.getBoundingClientRect();
        const containerRect = container.getBoundingClientRect();

        setIndicatorStyle({
          width: btnRect.width,
          left: btnRect.left - containerRect.left,
        });
      }
    };

    updateIndicator();
    window.addEventListener("resize", updateIndicator);
    return () => window.removeEventListener("resize", updateIndicator);
  }, [active]);

  return (
    <div className="fixed bottom-4 left-1/2 -translate-x-1/2 z-50 w-full max-w-lg px-2 mb-64">
      <div
        ref={containerRef}
        className="relative flex items-center justify-between bg-white dark:bg-neutral-900 shadow-xl rounded-full px-1 py-2 border border-gray-200 dark:border-gray-800"
      >
        {items.map((item, index) => (
          <button
            key={item.id}
            ref={(el) => (btnRefs.current[index] = el)}
            onClick={() => setActive(index)}
            className="relative flex flex-col items-center justify-center flex-1 px-2 py-2 text-sm font-medium text-gray-600 dark:text-gray-300"
          >
            <div className="z-10">{item.icon}</div>
            {/* hide labels on small screens */}
            <span className="text-xs mt-1 hidden sm:block">{item.label}</span>
          </button>
        ))}

        {/* Sliding Active Indicator */}
        <motion.div
          animate={indicatorStyle}
          transition={{ type: "spring", stiffness: 400, damping: 30 }}
          className="absolute top-1 bottom-1 rounded-full bg-blue-500/10 dark:bg-blue-400/20"
        />
      </div>
    </div>
  );
};

export default FloatingNav;
