https://21st.dev/community/components/uniquesonu/data-card-display/default
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
data-card-display.tsx
import React from 'react';
import { Card, CardHeader, CardContent, CardFooter, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
// Define the icon type. Using React.ElementType for flexibility.
type IconType = React.ElementType | React.FunctionComponent<React.SVGProps<SVGSVGElement>>;

// --- 📦 API (Props) Definition ---
export interface CardDisplayItem {
  /** A unique identifier for the card item. */
  id: string;
  /** Title of the card. */
  title: string;
  /** Main value or content of the card. */
  value: string;
  /** Detailed description or subtext. */
  description: string;
  /** Optional icon to display in the header. */
  icon?: IconType;
  /** Label for the optional footer action button. */
  actionLabel?: string;
  /** Disables the action button if true. */
  isDisabled?: boolean;
  /** Callback for when the action button is clicked. */
  onActionClick?: (id: string) => void;
}

export interface CardDisplayProps {
  /** Array of card items to display. */
  items: CardDisplayItem[];
  /** Optional class name to apply to the main container. */
  className?: string;
}

/**
 * A professional, monochrome, and responsive display for a collection of data cards.
 * Uses shadcn/ui components for styling, light/dark theme support, and accessibility.
 */
const CardDisplay: React.FC<CardDisplayProps> = ({ items, className }) => {
  if (!items || items.length === 0) {
    return <p className="text-center text-muted-foreground p-8">No display items configured.</p>;
  }

  return (
    <div
      className={cn(
        "grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 p-4 md:p-6",
        className
      )}
      role="list" // ARIA role for a list of cards
    >
      {items.map((item) => (
        <Card
          key={item.id}
          className="flex flex-col h-full transition-shadow duration-200 hover:shadow-lg focus-within:ring-2 focus-within:ring-primary focus-within:ring-offset-2"
          role="listitem" // ARIA role for a card item
        >
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium tracking-tight text-foreground">
              {item.title}
            </CardTitle>
            {item.icon && (
              <item.icon className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
            )}
          </CardHeader>
          <CardContent className="flex-grow">
            <div className="text-2xl font-bold mb-1 text-foreground">{item.value}</div>
            <CardDescription className="text-xs text-muted-foreground min-h-[1.5rem]">
              {item.description}
            </CardDescription>
          </CardContent>
          {item.actionLabel && (
            <CardFooter>
              <Button
                variant="outline"
                size="sm"
                onClick={() => item.onActionClick?.(item.id)}
                disabled={item.isDisabled}
                className="w-full text-sm font-semibold transition-colors duration-150 hover:bg-accent hover:text-accent-foreground"
                aria-label={`Action for ${item.title}: ${item.actionLabel}`}
              >
                {item.actionLabel}
              </Button>
            </CardFooter>
          )}
        </Card>
      ))}
    </div>
  );
};


import { Users, DollarSign, Clock, CheckCircle } from "lucide-react";

const ExampleUsage = () => {
  const mockData: CardDisplayItem[] = [
    {
      id: "users-active",
      title: "Active Users",
      value: "1,234",
      description: "+20.1% from last month",
      icon: Users,
      actionLabel: "View Report",
      onActionClick: (id) => console.log(`Action clicked for ID: ${id}`),
    },
    {
      id: "revenue-total",
      title: "Total Revenue",
      value: "$45,231.89",
      description: "Revenue year-to-date",
      icon: DollarSign,
      actionLabel: "Export Data",
      isDisabled: false,
      onActionClick: (id) => console.log(`Action clicked for ID: ${id}`),
    },
    {
      id: "avg-time",
      title: "Avg. Session Time",
      value: "12m 34s",
      description: "The average user session duration.",
      icon: Clock,
      actionLabel: "Analyze",
      onActionClick: (id) => console.log(`Action clicked for ID: ${id}`),
    },
    {
      id: "tasks-complete",
      title: "Tasks Completed",
      value: "95%",
      description: "Monthly task completion rate.",
      icon: CheckCircle,
      actionLabel: "Details",
      onActionClick: (id) => console.log(`Action clicked for ID: ${id}`),
    },
  ];

  return (
    <div className="p-4 bg-background">
      <h2 className="text-xl font-semibold mb-4 text-foreground">Dashboard Overview</h2>
      <CardDisplay items={mockData} className="max-w-7xl mx-auto" />
    </div>
  );
};

export default ExampleUsage; 

demo.tsx
import ExampleUsage from "@/components/ui/data-card-display";

export default function DemoOne() {
  return (
    <ExampleUsage />
  );
};

```

Copy-paste these files for dependencies:
```tsx
shadcn/card
import * as React from "react"

import { cn } from "@/lib/utils"

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-lg border bg-card text-card-foreground shadow-sm",
      className,
    )}
    {...props}
  />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1.5 p-6", className)}
    {...props}
  />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      "text-2xl font-semibold leading-none tracking-tight",
      className,
    )}
    {...props}
  />
))
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
))
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
))
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center p-6 pt-0", className)}
    {...props}
  />
))
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }

```
```tsx
shadcn/button
import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive:
          "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline:
          "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary:
          "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  },
)
Button.displayName = "Button"

export { Button, buttonVariants }

```

Install NPM dependencies:
```bash
lucide-react, @radix-ui/react-slot, class-variance-authority
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
 import React from 'react';
 import { Card, CardHeader, CardContent, CardFooter, CardTitle, CardDescription } from "@/components/ui/card";
 import { Button } from "@/components/ui/button";
 import { cn } from "@/lib/utils";
 // Define the icon type. Using React.ElementType for flexibility.
 type IconType = React.ElementType | React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
 
 // --- 📦 API (Props) Definition ---
 export interface CardDisplayItem {
   /** A unique identifier for the card item. */
   id: string;
   /** Title of the card. */
   title: string;
   /** Main value or content of the card. */
   value: string;
   /** Detailed description or subtext. */
   description: string;
   /** Optional icon to display in the header. */
   icon?: IconType;
   /** Label for the optional footer action button. */
   actionLabel?: string;
   /** Disables the action button if true. */
   isDisabled?: boolean;
   /** Callback for when the action button is clicked. */
   onActionClick?: (id: string) => void;
 }
 
 export interface CardDisplayProps {
   /** Array of card items to display. */
   items: CardDisplayItem[];
   /** Optional class name to apply to the main container. */
   className?: string;
 }
 
 /**
  * A professional, monochrome, and responsive display for a collection of data cards.
  * Uses shadcn/ui components for styling, light/dark theme support, and accessibility.
  */
 const CardDisplay: React.FC<CardDisplayProps> = ({ items, className }) => {
   if (!items || items.length === 0) {
     return <p className="text-center text-muted-foreground p-8">No display items configured.</p>;
   }
 
   return (
     <div
       className={cn(
         "grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 p-4 md:p-6",
         className
       )}
       role="list" // ARIA role for a list of cards
     >
       {items.map((item) => (
         <Card
           key={item.id}
           className="flex flex-col h-full transition-shadow duration-200 hover:shadow-lg focus-within:ring-2 focus-within:ring-primary focus-within:ring-offset-2"
           role="listitem" // ARIA role for a card item
         >
           <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
             <CardTitle className="text-sm font-medium tracking-tight text-foreground">
               {item.title}
             </CardTitle>
             {item.icon && (
               <item.icon className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
             )}
           </CardHeader>
           <CardContent className="flex-grow">
             <div className="text-2xl font-bold mb-1 text-foreground">{item.value}</div>
             <CardDescription className="text-xs text-muted-foreground min-h-[1.5rem]">
               {item.description}
             </CardDescription>
           </CardContent>
           {item.actionLabel && (
             <CardFooter>
               <Button
                 variant="outline"
                 size="sm"
                 onClick={() => item.onActionClick?.(item.id)}
                 disabled={item.isDisabled}
                 className="w-full text-sm font-semibold transition-colors duration-150 hover:bg-accent hover:text-accent-foreground"
                 aria-label={`Action for ${item.title}: ${item.actionLabel}`}
               >
                 {item.actionLabel}
               </Button>
             </CardFooter>
           )}
         </Card>
       ))}
     </div>
   );
 };
 
 
 import { Users, DollarSign, Clock, CheckCircle } from "lucide-react";
 
 const ExampleUsage = () => {
   const mockData: CardDisplayItem[] = [
     {
       id: "users-active",
       title: "Active Users",
       value: "1,234",
       description: "+20.1% from last month",
       icon: Users,
       actionLabel: "View Report",
       onActionClick: (id) => console.log(`Action clicked for ID: ${id}`),
     },
     {
       id: "revenue-total",
       title: "Total Revenue",
       value: "$45,231.89",
       description: "Revenue year-to-date",
       icon: DollarSign,
       actionLabel: "Export Data",
       isDisabled: false,
       onActionClick: (id) => console.log(`Action clicked for ID: ${id}`),
     },
     {
       id: "avg-time",
       title: "Avg. Session Time",
       value: "12m 34s",
       description: "The average user session duration.",
       icon: Clock,
       actionLabel: "Analyze",
       onActionClick: (id) => console.log(`Action clicked for ID: ${id}`),
     },
     {
       id: "tasks-complete",
       title: "Tasks Completed",
       value: "95%",
       description: "Monthly task completion rate.",
       icon: CheckCircle,
       actionLabel: "Details",
       onActionClick: (id) => console.log(`Action clicked for ID: ${id}`),
     },
   ];
 
   return (
     <div className="p-4 bg-background">
       <h2 className="text-xl font-semibold mb-4 text-foreground">Dashboard Overview</h2>
       <CardDisplay items={mockData} className="max-w-7xl mx-auto" />
     </div>
   );
 };
 
 export default ExampleUsage; 