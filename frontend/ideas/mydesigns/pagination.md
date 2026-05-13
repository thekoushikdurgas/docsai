https://21st.dev/community/components/anubra266/pagination/pagination-complete
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
pagination.tsx
"use client";

import { Pagination } from "@ark-ui/react/pagination";
import { ChevronLeft, ChevronRight } from "lucide-react";

export default function Basic() {
  return (
    <Pagination.Root
      count={100}
      pageSize={10}
      siblingCount={2}
      className="w-full border flex items-center justify-between"
    >
      <Pagination.PrevTrigger className="inline-flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300 text-sm font-medium rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 focus:outline-hidden focus:ring-2 focus:ring-blue-500/50 dark:focus:ring-blue-400/50 focus:ring-offset-2 transition-colors data-disabled:opacity-50 data-disabled:cursor-not-allowed data-disabled:pointer-events-none">
        <ChevronLeft className="w-4 h-4" />
        Previous
      </Pagination.PrevTrigger>
      <Pagination.NextTrigger className="inline-flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300 text-sm font-medium rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 focus:outline-hidden focus:ring-2 focus:ring-blue-500/50 dark:focus:ring-blue-400/50 focus:ring-offset-2 transition-colors data-disabled:opacity-50 data-disabled:cursor-not-allowed data-disabled:pointer-events-none">
        Next
        <ChevronRight className="w-4 h-4" />
      </Pagination.NextTrigger>
    </Pagination.Root>
  );
}


demo.tsx
"use client";

import { Pagination } from "@ark-ui/react/pagination";
import {
  ChevronLeft,
  ChevronRight,
  ChevronsLeft,
  ChevronsRight,
} from "lucide-react";

export default function Complete() {
  return (
    <Pagination.Root
      count={500}
      pageSize={10}
      siblingCount={1}
      className="flex items-center gap-1"
    >
      <Pagination.Context>
        {(pagination) => (
          <button
            onClick={() => pagination.goToFirstPage()}
            disabled={pagination.page === 1}
            className="inline-flex items-center justify-center w-8 h-8 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none"
          >
            <ChevronsLeft className="w-4 h-4" />
          </button>
        )}
      </Pagination.Context>

      <Pagination.PrevTrigger className="inline-flex items-center justify-center w-8 h-8 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md transition-colors data-disabled:opacity-50 data-disabled:cursor-not-allowed data-disabled:pointer-events-none">
        <ChevronLeft className="w-4 h-4" />
      </Pagination.PrevTrigger>

      <Pagination.Context>
        {(pagination) =>
          pagination.pages.map((page, index) =>
            page.type === "page" ? (
              <Pagination.Item
                key={index}
                {...page}
                className="inline-flex items-center justify-center w-8 h-8 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md transition-colors data-selected:bg-blue-500 data-selected:text-white data-selected:hover:bg-blue-600"
              >
                {page.value}
              </Pagination.Item>
            ) : (
              <Pagination.Ellipsis
                key={index}
                index={index}
                className="inline-flex items-center justify-center w-8 h-8 text-gray-500 dark:text-gray-400"
              >
                &#8230;
              </Pagination.Ellipsis>
            )
          )
        }
      </Pagination.Context>

      <Pagination.NextTrigger className="inline-flex items-center justify-center w-8 h-8 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md transition-colors data-disabled:opacity-50 data-disabled:cursor-not-allowed data-disabled:pointer-events-none">
        <ChevronRight className="w-4 h-4" />
      </Pagination.NextTrigger>

      <Pagination.Context>
        {(pagination) => (
          <button
            onClick={() => pagination.goToLastPage()}
            disabled={pagination.page === pagination.totalPages}
            className="inline-flex items-center justify-center w-8 h-8 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none"
          >
            <ChevronsRight className="w-4 h-4" />
          </button>
        )}
      </Pagination.Context>
    </Pagination.Root>
  );
}

```

Install NPM dependencies:
```bash
lucide-react, @ark-ui/react
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

import { Pagination } from "@ark-ui/react/pagination";
import { ChevronLeft, ChevronRight } from "lucide-react";

export default function Basic() {
  return (
    <Pagination.Root
      count={100}
      pageSize={10}
      siblingCount={2}
      className="w-full border flex items-center justify-between"
    >
      <Pagination.PrevTrigger className="inline-flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300 text-sm font-medium rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 focus:outline-hidden focus:ring-2 focus:ring-blue-500/50 dark:focus:ring-blue-400/50 focus:ring-offset-2 transition-colors data-disabled:opacity-50 data-disabled:cursor-not-allowed data-disabled:pointer-events-none">
        <ChevronLeft className="w-4 h-4" />
        Previous
      </Pagination.PrevTrigger>
      <Pagination.NextTrigger className="inline-flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300 text-sm font-medium rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 focus:outline-hidden focus:ring-2 focus:ring-blue-500/50 dark:focus:ring-blue-400/50 focus:ring-offset-2 transition-colors data-disabled:opacity-50 data-disabled:cursor-not-allowed data-disabled:pointer-events-none">
        Next
        <ChevronRight className="w-4 h-4" />
      </Pagination.NextTrigger>
    </Pagination.Root>
  );
}
