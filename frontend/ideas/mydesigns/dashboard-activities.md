https://21st.dev/community/components/shadcnspace/shadcn-accordion/default
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
shadcn-accordion.tsx
"use client";

import { useState } from "react";
import { format } from "date-fns";
import { CalendarIcon, Clock, ChevronDown, Check } from "lucide-react";
import { cn } from "@/lib/utils";

import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

const DateAndTimePickerDemo = () => {
  const [open, setOpen] = useState(false);
  const [date, setDate] = useState<Date | undefined>(undefined);
  const [bookingStatus, setBookingStatus] = useState<
    "idle" | "loading" | "success"
  >("idle");

  const handleBooking = () => {
    setBookingStatus("loadi
    setTimeout(() => setBookingStatus("success"), 1500);
  };

  return (
    <>
      <div className="grid gap-6">
        <div className="grid gap-2">
          <Label htmlFor="date" className="text-sm font-semibold">
            Select Date
          </Label>
          <Popover open={open} onOpenChange={setOpen}>
            <PopoverTrigger
              onPointerDown={() => setBookingStatus("idle")}
              render={
                <Button
                  variant="outline"
                  id="date"
                  className={cn(
                    "w-full justify-start text-left font-normal h-10 transition-all hover:bg-muted/50 cursor-pointer",
                    !date && "text-muted-foreground",
                  )}
                >
                  <CalendarIcon className="mr-2 h-4 w-4 opacity-70" />
                  {date ? format(date, "PPP") : <span>Select a date</span>}
                  <ChevronDown className="ml-auto h-4 w-4 opacity-50" />
                </Button>
              }
            />
            <PopoverContent
              className="w-auto p-0 border-muted-foreground/10 shadow-2xl"
              align="start"
            >
              <Calendar
                mode="single"
                selected={date}
                onSelect={(d) => {
                  setDate(d);
                  setOpen(false);
                }}
                className="rounded-md border-none"
              />
            </PopoverContent>
          </Popover>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="grid gap-2">
            <Label
              htmlFor="time-from"
              className="text-sm font-semibold text-muted-foreground flex items-center gap-1.5"
            >
              <Clock className="size-3.5" /> Start Time
            </Label>
            <Input
              type="time"
              id="time-from"
              defaultValue="09:00"
              className="h-10 bg-background appearance-none transition-all focus:ring-2 focus:ring-primary/20"
            />
          </div>
          <div className="grid gap-2">
            <Label
              htmlFor="time-to"
              className="text-sm font-semibold text-muted-foreground flex items-center gap-1.5"
            >
              <Clock className="size-3.5" /> End Time
            </Label>
            <Input
              type="time"
              id="time-to"
              defaultValue="10:00"
              className="h-10 bg-background appearance-none transition-all focus:ring-2 focus:ring-primary/20"
            />
          </div>
        </div>

        <Button
          className="w-full h-11 font-semibold transition-all group overflow-hidden relative cursor-pointer"
          onClick={handleBooking}
          disabled={!date || bookingStatus !== "idle"}
        >
          {bookingStatus === "idle" && (
            <span className="flex items-center gap-2">Confirm Meet</span>
          )}
          {bookingStatus === "loading" && (
            <div className="flex items-center gap-2">
              <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
              Processing...
            </div>
          )}
          {bookingStatus === "success" && (
            <span className="flex items-center gap-2 animate-in zoom-in-50 duration-300">
              <Check className="h-4 w-4" />
              Meet Scheduled!
            </span>
          )}
        </Button>
      </div>
    </>
  );
};

export default DateAndTimePickerDemo;


demo.tsx
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { cn } from "@/lib/utils";
import { FileText, Folder, LucideIcon, Settings, Users } from "lucide-react";

const data: {
  value: string;
  title: string;
  subtitle: string;
  content: string;
  icon: LucideIcon;
  textColor: string;
  bgColor: string;
}[] = [
  {
    value: "documents",
    title: "Documents",
    subtitle: "Manage your files",
    content:
      "View, upload, and organize all your documents in one place. Keep everything structured and easy to find.",
    icon: FileText,
    textColor: "text-blue-500",
    bgColor: "bg-blue-500/10",
  },
  {
    value: "projects",
    title: "Projects",
    subtitle: "Organize your work",
    content:
      "Group related files and tasks into projects to keep your workflow clean and efficient.",
    icon: Folder,
    textColor: "text-orange-400",
    bgColor: "bg-orange-400/10",
  },
  {
    value: "settings",
    title: "Settings",
    subtitle: "Customize your experience",
    content:
      "Adjust preferences, update account details, and configure application behavior.",
    icon: Settings,
    textColor: "text-teal-400",
    bgColor: "bg-teal-400/10",
  },
  {
    value: "team",
    title: "Team Members",
    subtitle: "Manage users and roles",
    content:
      "Invite new members, assign roles, and control access permissions for your team.",
    icon: Users,
    textColor: "text-red-500",
    bgColor: "bg-red-500/10",
  },
];

const AccordionDemo = () => (
  <div className="flex items-center justify-center max-w-md w-full">
    <Accordion
      className="w-full -space-y-px"
      defaultValue={[data[0].value]}
    >
      {data.map((item) => {
        const Icon = item.icon;
        return (
          <AccordionItem
            key={item.value}
            value={item.value}
            className=" border bg-background px-4 first:rounded-t-lg last:rounded-b-lg last:border-b"
          >
            <AccordionTrigger className="hover:no-underline">
              <div className="flex items-center gap-3">
                <div
                  className={cn(
                    "p-2.5 rounded-xl",
                    item.bgColor,
                    item.textColor
                  )}
                >
                  <Icon size={20} className="size-5" />
                </div>
                <div className="flex flex-col items-start text-left">
                  <span>{item.title}</span>
                  <span className="text-sm text-muted-foreground">
                    {item.subtitle}
                  </span>
                </div>
              </div>
            </AccordionTrigger>
            <AccordionContent className="ps-14">
              <p className="text-muted-foreground">{item.content}</p>
            </AccordionContent>
          </AccordionItem>
        );
      })}
    </Accordion>
  </div>
);

export default AccordionDemo;

```

Copy-paste these files for dependencies:
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
shadcn/label
"use client"

import * as React from "react"
import * as LabelPrimitive from "@radix-ui/react-label"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const labelVariants = cva(
  "text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
)

const Label = React.forwardRef<
  React.ElementRef<typeof LabelPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof LabelPrimitive.Root> &
    VariantProps<typeof labelVariants>
>(({ className, ...props }, ref) => (
  <LabelPrimitive.Root
    ref={ref}
    className={cn(labelVariants(), className)}
    {...props}
  />
))
Label.displayName = LabelPrimitive.Root.displayName

export { Label }

```
```tsx
shadcn/accordion
"use client"

import * as React from "react"
import * as AccordionPrimitive from "@radix-ui/react-accordion"
import { ChevronDown } from "lucide-react"

import { cn } from "@/lib/utils"

const Accordion = AccordionPrimitive.Root

const AccordionItem = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Item>
>(({ className, ...props }, ref) => (
  <AccordionPrimitive.Item
    ref={ref}
    className={cn("border-b", className)}
    {...props}
  />
))
AccordionItem.displayName = "AccordionItem"

const AccordionTrigger = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Trigger>
>(({ className, children, ...props }, ref) => (
  <AccordionPrimitive.Header className="flex">
    <AccordionPrimitive.Trigger
      ref={ref}
      className={cn(
        "flex flex-1 items-center justify-between py-4 font-medium transition-all hover:underline [&[data-state=open]>svg]:rotate-180",
        className,
      )}
      {...props}
    >
      {children}
      <ChevronDown className="h-4 w-4 shrink-0 transition-transform duration-200" />
    </AccordionPrimitive.Trigger>
  </AccordionPrimitive.Header>
))
AccordionTrigger.displayName = AccordionPrimitive.Trigger.displayName

const AccordionContent = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <AccordionPrimitive.Content
    ref={ref}
    className="overflow-hidden text-sm transition-all data-[state=closed]:animate-accordion-up data-[state=open]:animate-accordion-down"
    {...props}
  >
    <div className={cn("pb-4 pt-0", className)}>{children}</div>
  </AccordionPrimitive.Content>
))

AccordionContent.displayName = AccordionPrimitive.Content.displayName

export { Accordion, AccordionItem, AccordionTrigger, AccordionContent }

```

Install NPM dependencies:
```bash
@radix-ui/react-slot, class-variance-authority, @radix-ui/react-label, lucide-react, @radix-ui/react-accordion
```

Extend existing Tailwind 4 index.css with this code (or if project uses Tailwind 3, extend tailwind.config.js or globals.css):
```css
@import "tailwindcss";
@import "tw-animate-css";

@theme inline {
  --animate-accordion-down: accordion-down 0.2s ease-out;
  --animate-accordion-up: accordion-up 0.2s ease-out;
}


@keyframes accordion-down {
  from {
    height: 0;
  }
  to {
    height: var(--radix-accordion-content-height);
  }
}

@keyframes accordion-up {
  from {
    height: var(--radix-accordion-content-height);
  }
  to {
    height: 0;
  }
}
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

import { useState } from "react";
import { format } from "date-fns";
import { CalendarIcon, Clock, ChevronDown, Check } from "lucide-react";
import { cn } from "@/lib/utils";

import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

const DateAndTimePickerDemo = () => {
  const [open, setOpen] = useState(false);
  const [date, setDate] = useState<Date | undefined>(undefined);
  const [bookingStatus, setBookingStatus] = useState<
    "idle" | "loading" | "success"
  >("idle");

  const handleBooking = () => {
    setBookingStatus("loadi
    setTimeout(() => setBookingStatus("success"), 1500);
  };

  return (
    <>
      <div className="grid gap-6">
        <div className="grid gap-2">
          <Label htmlFor="date" className="text-sm font-semibold">
            Select Date
          </Label>
          <Popover open={open} onOpenChange={setOpen}>
            <PopoverTrigger
              onPointerDown={() => setBookingStatus("idle")}
              render={
                <Button
                  variant="outline"
                  id="date"
                  className={cn(
                    "w-full justify-start text-left font-normal h-10 transition-all hover:bg-muted/50 cursor-pointer",
                    !date && "text-muted-foreground",
                  )}
                >
                  <CalendarIcon className="mr-2 h-4 w-4 opacity-70" />
                  {date ? format(date, "PPP") : <span>Select a date</span>}
                  <ChevronDown className="ml-auto h-4 w-4 opacity-50" />
                </Button>
              }
            />
            <PopoverContent
              className="w-auto p-0 border-muted-foreground/10 shadow-2xl"
              align="start"
            >
              <Calendar
                mode="single"
                selected={date}
                onSelect={(d) => {
                  setDate(d);
                  setOpen(false);
                }}
                className="rounded-md border-none"
              />
            </PopoverContent>
          </Popover>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="grid gap-2">
            <Label
              htmlFor="time-from"
              className="text-sm font-semibold text-muted-foreground flex items-center gap-1.5"
            >
              <Clock className="size-3.5" /> Start Time
            </Label>
            <Input
              type="time"
              id="time-from"
              defaultValue="09:00"
              className="h-10 bg-background appearance-none transition-all focus:ring-2 focus:ring-primary/20"
            />
          </div>
          <div className="grid gap-2">
            <Label
              htmlFor="time-to"
              className="text-sm font-semibold text-muted-foreground flex items-center gap-1.5"
            >
              <Clock className="size-3.5" /> End Time
            </Label>
            <Input
              type="time"
              id="time-to"
              defaultValue="10:00"
              className="h-10 bg-background appearance-none transition-all focus:ring-2 focus:ring-primary/20"
            />
          </div>
        </div>

        <Button
          className="w-full h-11 font-semibold transition-all group overflow-hidden relative cursor-pointer"
          onClick={handleBooking}
          disabled={!date || bookingStatus !== "idle"}
        >
          {bookingStatus === "idle" && (
            <span className="flex items-center gap-2">Confirm Meet</span>
          )}
          {bookingStatus === "loading" && (
            <div className="flex items-center gap-2">
              <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
              Processing...
            </div>
          )}
          {bookingStatus === "success" && (
            <span className="flex items-center gap-2 animate-in zoom-in-50 duration-300">
              <Check className="h-4 w-4" />
              Meet Scheduled!
            </span>
          )}
        </Button>
      </div>
    </>
  );
};

export default DateAndTimePickerDemo;
