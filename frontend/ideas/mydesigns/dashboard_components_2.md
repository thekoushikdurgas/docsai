https://21st.dev/community/components/ravikatiyar/dashboard-1/default
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
dashboard-1.tsx
import * as React from "react";
import { motion, useMotionValue, useTransform, animate } from "framer-motion";
import { Filter, Users, Clock, Zap, ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils"; // Your utility for merging class names
import { Button } from "@/components/ui/button"; // Assuming you have a Button component
import { Card, CardContent } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

// Type definitions for component props
interface ActivityStat {
  label: string;
  value: number; // Represents percentage
  color: string; // Tailwind color class e.g., 'bg-green-400'
}

interface TeamMember {
  id: string;
  name: string;
  avatarUrl: string;
}

interface MarketingDashboardProps {
  title?: string;
  teamActivities: {
    totalHours: number;
    stats: ActivityStat[];
  };
  team: {
    memberCount: number;
    members: TeamMember[];
  };
  cta: {
    text: string;
    buttonText: string;
    onButtonClick: () => void;
  };
  onFilterClick?: () => void;
  className?: string;
}

// Sub-component for animating numbers
const AnimatedNumber = ({ value }: { value: number }) => {
  const count = useMotionValue(0);
  const rounded = useTransform(count, (latest) => Math.round(latest * 10) / 10); // Format to one decimal place

  React.useEffect(() => {
    const controls = animate(count, value, {
      duration: 1.5,
      ease: "easeOut",
    });
    return controls.stop;
  }, [value, count]);

  return <motion.span>{rounded}</motion.span>;
};

// Main Component
export const MarketingDashboard = React.forwardRef<
  HTMLDivElement,
  MarketingDashboardProps
>(({ 
  title = "Marketing Activities",
  teamActivities,
  team,
  cta,
  onFilterClick,
  className 
}, ref) => {
  
  // Animation variants for Framer Motion
  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 15 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
  };

  const hoverTransition = { type: "spring", stiffness: 300, damping: 15 };

  return (
    <motion.div
      ref={ref}
      className={cn("w-full max-w-2xl p-6 bg-card text-card-foreground rounded-2xl border", className)}
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Header */}
      <motion.div variants={itemVariants} className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">{title}</h2>
        <Button variant="ghost" size="icon" onClick={onFilterClick} aria-label="Filter activities">
          <Filter className="w-5 h-5" />
        </Button>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        {/* Team Activities Card */}
        <motion.div 
          variants={itemVariants} 
          whileHover={{ scale: 1.03, y: -5 }} // Added for hover effect
          transition={hoverTransition} // Added for hover effect
        >
          <Card className="h-full p-4 overflow-hidden rounded-xl">
            <CardContent className="p-2">
              <div className="flex items-center justify-between mb-4">
                <p className="font-medium text-muted-foreground">Team Activities</p>
                <Clock className="w-5 h-5 text-muted-foreground" />
              </div>
              <div className="mb-4">
                <span className="text-4xl font-bold">
                  <AnimatedNumber value={teamActivities.totalHours} />
                </span>
                <span className="ml-1 text-muted-foreground">hours</span>
              </div>
              {/* Progress Bar */}
              <div className="w-full h-2 mb-2 overflow-hidden rounded-full bg-muted flex">
                {teamActivities.stats.map((stat, index) => (
                  <motion.div
                    key={index}
                    className={cn("h-full", stat.color)}
                    initial={{ width: 0 }}
                    animate={{ width: `${stat.value}%` }}
                    transition={{ duration: 1, delay: 0.5 + index * 0.1 }}
                  />
                ))}
              </div>
              {/* Legend */}
              <div className="flex items-center justify-between text-xs text-muted-foreground">
                {teamActivities.stats.map((stat) => (
                  <div key={stat.label} className="flex items-center gap-1.5">
                    <span className={cn("w-2 h-2 rounded-full", stat.color)}></span>
                    <span>{stat.label}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Team Members Card */}
        <motion.div 
          variants={itemVariants}
          whileHover={{ scale: 1.03, y: -5 }} // Added for hover effect
          transition={hoverTransition} // Added for hover effect
        >
          <Card className="h-full p-4 overflow-hidden rounded-xl bg-lime-50 dark:bg-lime-900/30 border-lime-200 dark:border-lime-800">
            <CardContent className="p-2">
              <div className="flex items-center justify-between mb-4">
                <p className="font-medium text-lime-900 dark:text-lime-200">Team</p>
                <Users className="w-5 h-5 text-lime-900 dark:text-lime-200" />
              </div>
              <div className="mb-6">
                <span className="text-4xl font-bold text-lime-950 dark:text-lime-50">
                   <AnimatedNumber value={team.memberCount} />
                </span>
                <span className="ml-1 text-lime-800 dark:text-lime-300">members</span>
              </div>
              {/* Avatar Stack */}
              <div className="flex -space-x-2">
                {team.members.slice(0, 4).map((member, index) => (
                  <motion.div
                    key={member.id}
                    initial={{ opacity: 0, scale: 0.5 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.5, delay: 0.8 + index * 0.1 }}
                    whileHover={{ scale: 1.2, zIndex: 10, y: -2 }} // Added for hover effect
                  >
                    <Avatar className="border-2 border-lime-100 dark:border-lime-900">
                      <AvatarImage src={member.avatarUrl} alt={member.name} />
                      <AvatarFallback>{member.name.charAt(0)}</AvatarFallback>
                    </Avatar>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* CTA Banner */}
      <motion.div 
        variants={itemVariants} 
        whileHover={{ scale: 1.02 }} // Added for hover effect
        transition={hoverTransition} // Added for hover effect
        className="mt-4"
      >
         <div className="flex items-center justify-between p-4 rounded-xl bg-muted/60">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-full bg-background">
                  <Zap className="w-5 h-5 text-foreground" />
              </div>
              <p className="text-sm font-medium text-muted-foreground">{cta.text}</p>
            </div>
            <Button onClick={cta.onButtonClick} className="shrink-0">
                {cta.buttonText}
                <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
         </div>
      </motion.div>
    </motion.div>
  );
});

MarketingDashboard.displayName = "MarketingDashboard";

demo.tsx
import { MarketingDashboard } from "@/components/ui/dashboard-1"; // Adjust the import path

const MarketingDashboardDemo = () => {
  // Sample data to pass into the component
  const sampleTeamActivities = {
    totalHours: 16.5,
    stats: [
      { label: "Productive", value: 45, color: "bg-green-400" },
      { label: "Middle", value: 25, color: "bg-lime-300" },
      { label: "Break", value: 15, color: "bg-yellow-300" },
      { label: "Idle", value: 15, color: "bg-slate-800 dark:bg-slate-700" },
    ],
  };

  const sampleTeam = {
    memberCount: 235,
    members: [
      { id: "1", name: "Olivia Martin", avatarUrl: "https://i.pravatar.cc/150?u=a042581f4e29026024d" },
      { id: "2", name: "Jackson Lee", avatarUrl: "https://i.pravatar.cc/150?u=a042581f4e29026704d" },
      { id: "3", name: "Isabella Nguyen", avatarUrl: "https://i.pravatar.cc/150?u=a04258114e29026302d" },
      { id: "4", name: "William Kim", avatarUrl: "https://i.pravatar.cc/150?u=a04258114e29026702d" },
    ],
  };

  const sampleCta = {
    text: "Manage your activities and team members",
    buttonText: "See All",
    onButtonClick: () => alert("'See All' button clicked!"),
  };

  return (
    <div className="flex items-center justify-center min-h-screen p-4 bg-background">
      <MarketingDashboard
        teamActivities={sampleTeamActivities}
        team={sampleTeam}
        cta={sampleCta}
        onFilterClick={() => alert("Filter clicked!")}
      />
    </div>
  );
};

export default MarketingDashboardDemo;
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
```tsx
originui/avatar
"use client";

import * as AvatarPrimitive from "@radix-ui/react-avatar";
import * as React from "react";

import { cn } from "@/lib/utils";

const Avatar = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Root>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Root
    ref={ref}
    className={cn("relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full", className)}
    {...props}
  />
));
Avatar.displayName = AvatarPrimitive.Root.displayName;

const AvatarImage = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Image>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Image>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Image
    ref={ref}
    className={cn("aspect-square h-full w-full", className)}
    {...props}
  />
));
AvatarImage.displayName = AvatarPrimitive.Image.displayName;

const AvatarFallback = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Fallback>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Fallback>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Fallback
    ref={ref}
    className={cn(
      "flex h-full w-full items-center justify-center rounded-[inherit] bg-secondary text-xs",
      className,
    )}
    {...props}
  />
));
AvatarFallback.displayName = AvatarPrimitive.Fallback.displayName;

export { Avatar, AvatarFallback, AvatarImage };

```

Install NPM dependencies:
```bash
lucide-react, framer-motion, @radix-ui/react-slot, class-variance-authority, @radix-ui/react-avatar
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
import * as React from "react";
import { motion, useMotionValue, useTransform, animate } from "framer-motion";
import { Filter, Users, Clock, Zap, ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils"; // Your utility for merging class names
import { Button } from "@/components/ui/button"; // Assuming you have a Button component
import { Card, CardContent } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

// Type definitions for component props
interface ActivityStat {
  label: string;
  value: number; // Represents percentage
  color: string; // Tailwind color class e.g., 'bg-green-400'
}

interface TeamMember {
  id: string;
  name: string;
  avatarUrl: string;
}

interface MarketingDashboardProps {
  title?: string;
  teamActivities: {
    totalHours: number;
    stats: ActivityStat[];
  };
  team: {
    memberCount: number;
    members: TeamMember[];
  };
  cta: {
    text: string;
    buttonText: string;
    onButtonClick: () => void;
  };
  onFilterClick?: () => void;
  className?: string;
}

// Sub-component for animating numbers
const AnimatedNumber = ({ value }: { value: number }) => {
  const count = useMotionValue(0);
  const rounded = useTransform(count, (latest) => Math.round(latest * 10) / 10); // Format to one decimal place

  React.useEffect(() => {
    const controls = animate(count, value, {
      duration: 1.5,
      ease: "easeOut",
    });
    return controls.stop;
  }, [value, count]);

  return <motion.span>{rounded}</motion.span>;
};

// Main Component
export const MarketingDashboard = React.forwardRef<
  HTMLDivElement,
  MarketingDashboardProps
>(({ 
  title = "Marketing Activities",
  teamActivities,
  team,
  cta,
  onFilterClick,
  className 
}, ref) => {
  
  // Animation variants for Framer Motion
  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 15 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
  };

  const hoverTransition = { type: "spring", stiffness: 300, damping: 15 };

  return (
    <motion.div
      ref={ref}
      className={cn("w-full max-w-2xl p-6 bg-card text-card-foreground rounded-2xl border", className)}
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Header */}
      <motion.div variants={itemVariants} className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">{title}</h2>
        <Button variant="ghost" size="icon" onClick={onFilterClick} aria-label="Filter activities">
          <Filter className="w-5 h-5" />
        </Button>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        {/* Team Activities Card */}
        <motion.div 
          variants={itemVariants} 
          whileHover={{ scale: 1.03, y: -5 }} // Added for hover effect
          transition={hoverTransition} // Added for hover effect
        >
          <Card className="h-full p-4 overflow-hidden rounded-xl">
            <CardContent className="p-2">
              <div className="flex items-center justify-between mb-4">
                <p className="font-medium text-muted-foreground">Team Activities</p>
                <Clock className="w-5 h-5 text-muted-foreground" />
              </div>
              <div className="mb-4">
                <span className="text-4xl font-bold">
                  <AnimatedNumber value={teamActivities.totalHours} />
                </span>
                <span className="ml-1 text-muted-foreground">hours</span>
              </div>
              {/* Progress Bar */}
              <div className="w-full h-2 mb-2 overflow-hidden rounded-full bg-muted flex">
                {teamActivities.stats.map((stat, index) => (
                  <motion.div
                    key={index}
                    className={cn("h-full", stat.color)}
                    initial={{ width: 0 }}
                    animate={{ width: `${stat.value}%` }}
                    transition={{ duration: 1, delay: 0.5 + index * 0.1 }}
                  />
                ))}
              </div>
              {/* Legend */}
              <div className="flex items-center justify-between text-xs text-muted-foreground">
                {teamActivities.stats.map((stat) => (
                  <div key={stat.label} className="flex items-center gap-1.5">
                    <span className={cn("w-2 h-2 rounded-full", stat.color)}></span>
                    <span>{stat.label}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Team Members Card */}
        <motion.div 
          variants={itemVariants}
          whileHover={{ scale: 1.03, y: -5 }} // Added for hover effect
          transition={hoverTransition} // Added for hover effect
        >
          <Card className="h-full p-4 overflow-hidden rounded-xl bg-lime-50 dark:bg-lime-900/30 border-lime-200 dark:border-lime-800">
            <CardContent className="p-2">
              <div className="flex items-center justify-between mb-4">
                <p className="font-medium text-lime-900 dark:text-lime-200">Team</p>
                <Users className="w-5 h-5 text-lime-900 dark:text-lime-200" />
              </div>
              <div className="mb-6">
                <span className="text-4xl font-bold text-lime-950 dark:text-lime-50">
                   <AnimatedNumber value={team.memberCount} />
                </span>
                <span className="ml-1 text-lime-800 dark:text-lime-300">members</span>
              </div>
              {/* Avatar Stack */}
              <div className="flex -space-x-2">
                {team.members.slice(0, 4).map((member, index) => (
                  <motion.div
                    key={member.id}
                    initial={{ opacity: 0, scale: 0.5 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.5, delay: 0.8 + index * 0.1 }}
                    whileHover={{ scale: 1.2, zIndex: 10, y: -2 }} // Added for hover effect
                  >
                    <Avatar className="border-2 border-lime-100 dark:border-lime-900">
                      <AvatarImage src={member.avatarUrl} alt={member.name} />
                      <AvatarFallback>{member.name.charAt(0)}</AvatarFallback>
                    </Avatar>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* CTA Banner */}
      <motion.div 
        variants={itemVariants} 
        whileHover={{ scale: 1.02 }} // Added for hover effect
        transition={hoverTransition} // Added for hover effect
        className="mt-4"
      >
         <div className="flex items-center justify-between p-4 rounded-xl bg-muted/60">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-full bg-background">
                  <Zap className="w-5 h-5 text-foreground" />
              </div>
              <p className="text-sm font-medium text-muted-foreground">{cta.text}</p>
            </div>
            <Button onClick={cta.onButtonClick} className="shrink-0">
                {cta.buttonText}
                <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
         </div>
      </motion.div>
    </motion.div>
  );
});

MarketingDashboard.displayName = "MarketingDashboard";