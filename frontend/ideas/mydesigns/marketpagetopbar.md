https://21st.dev/community/components/ruixenui/app-menu-bar/default
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
app-menu-bar.tsx
"use client";

import {
  Menubar,
  MenubarContent,
  MenubarItem,
  MenubarMenu,
  MenubarSeparator,
  MenubarTrigger,
  MenubarSub,
  MenubarSubTrigger,
  MenubarSubContent,
} from "@/components/ui/menubar";
import {
  Folder,
  FolderPlus,
  FileText,
  Users,
  UserCheck,
  Settings,
  Bell,
  Calendar,
  ChevronRight,
  CheckCircle,
  Upload,
} from "lucide-react";

export default function AppMenuBar() {
  return (
    <Menubar className="bg-white border-b border-slate-200 shadow-sm rounded-b-lg">
      {/* Projects Menu */}
      <MenubarMenu>
        <MenubarTrigger className="flex items-center gap-2">
          <Folder className="w-4 h-4" />
          Projects
        </MenubarTrigger>
        <MenubarContent className="w-56">
          <MenubarItem className="flex items-center gap-2">
            <FolderPlus className="w-4 h-4" />
            New Project
          </MenubarItem>
          <MenubarItem className="flex items-center gap-2">
            <FileText className="w-4 h-4" />
            All Projects
          </MenubarItem>
          <MenubarItem className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4" />
            Completed Projects
          </MenubarItem>
        </MenubarContent>
      </MenubarMenu>

      {/* Teams Menu with Submenu */}
      <MenubarMenu>
        <MenubarTrigger className="flex items-center gap-2">
          <Users className="w-4 h-4" />
          Teams
        </MenubarTrigger>
        <MenubarContent className="w-56">
          <MenubarItem className="flex items-center gap-2">
            <UserCheck className="w-4 h-4" />
            All Members
          </MenubarItem>
          <MenubarItem className="flex items-center gap-2">
            <FolderPlus className="w-4 h-4" />
            Create Team
          </MenubarItem>

          <MenubarSeparator />

          {/* Proper Nested Submenu */}
          <MenubarSub>
            <MenubarSubTrigger className="flex items-center justify-between gap-2">
              Manage Teams
            </MenubarSubTrigger>
            <MenubarSubContent className="w-48">
              <MenubarItem className="flex items-center gap-2">
                <Settings className="w-4 h-4" />
                Team Settings
              </MenubarItem>
              <MenubarItem className="flex items-center gap-2">
                <Users className="w-4 h-4" />
                Team Members
              </MenubarItem>
            </MenubarSubContent>
          </MenubarSub>
        </MenubarContent>
      </MenubarMenu>

      {/* Calendar Menu */}
      <MenubarMenu>
        <MenubarTrigger className="flex items-center gap-2">
          <Calendar className="w-4 h-4" />
          Calendar
        </MenubarTrigger>
        <MenubarContent className="w-48">
          <MenubarItem className="flex items-center gap-2">
            <Calendar className="w-4 h-4" />
            View Calendar
          </MenubarItem>
          <MenubarItem className="flex items-center gap-2">
            <FileText className="w-4 h-4" />
            Schedule Task
          </MenubarItem>
        </MenubarContent>
      </MenubarMenu>

      {/* Notifications */}
      <MenubarMenu>
        <MenubarTrigger className="flex items-center gap-2">
          <Bell className="w-4 h-4" />
          Notifications
        </MenubarTrigger>
        <MenubarContent className="w-48">
          <MenubarItem className="flex items-center gap-2">
            <Bell className="w-4 h-4" />
            All Notifications
          </MenubarItem>
        </MenubarContent>
      </MenubarMenu>

      {/* Files Menu */}
      <MenubarMenu>
        <MenubarTrigger className="flex items-center gap-2">
          <Upload className="w-4 h-4" />
          Files
        </MenubarTrigger>
        <MenubarContent className="w-56">
          <MenubarItem className="flex items-center gap-2">
            <Upload className="w-4 h-4" />
            Upload File
          </MenubarItem>
          <MenubarItem className="flex items-center gap-2">
            <FileText className="w-4 h-4" />
            My Files
          </MenubarItem>
        </MenubarContent>
      </MenubarMenu>
    </Menubar>
  );
}


demo.tsx
"use client";

import AppMenuBar from "@/components/ui/app-menu-bar";

export default function MenuDemoPage() {
  return (
    <div className="p-6">
      <AppMenuBar />
    </div>
  );
}

```

Copy-paste these files for dependencies:
```tsx
shadcn/menubar
"use client"

import * as React from "react"
import * as MenubarPrimitive from "@radix-ui/react-menubar"
import { Check, ChevronRight, Circle } from "lucide-react"

import { cn } from "@/lib/utils"

const MenubarMenu = MenubarPrimitive.Menu

const MenubarGroup = MenubarPrimitive.Group

const MenubarPortal = MenubarPrimitive.Portal

const MenubarSub = MenubarPrimitive.Sub

const MenubarRadioGroup = MenubarPrimitive.RadioGroup

const Menubar = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Root>
>(({ className, ...props }, ref) => (
  <MenubarPrimitive.Root
    ref={ref}
    className={cn(
      "flex h-10 items-center space-x-1 rounded-md border bg-background p-1",
      className,
    )}
    {...props}
  />
))
Menubar.displayName = MenubarPrimitive.Root.displayName

const MenubarTrigger = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Trigger>
>(({ className, ...props }, ref) => (
  <MenubarPrimitive.Trigger
    ref={ref}
    className={cn(
      "flex cursor-default select-none items-center rounded-sm px-3 py-1.5 text-sm font-medium outline-none focus:bg-accent focus:text-accent-foreground data-[state=open]:bg-accent data-[state=open]:text-accent-foreground",
      className,
    )}
    {...props}
  />
))
MenubarTrigger.displayName = MenubarPrimitive.Trigger.displayName

const MenubarSubTrigger = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.SubTrigger>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.SubTrigger> & {
    inset?: boolean
  }
>(({ className, inset, children, ...props }, ref) => (
  <MenubarPrimitive.SubTrigger
    ref={ref}
    className={cn(
      "flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[state=open]:bg-accent data-[state=open]:text-accent-foreground",
      inset && "pl-8",
      className,
    )}
    {...props}
  >
    {children}
    <ChevronRight className="ml-auto h-4 w-4" />
  </MenubarPrimitive.SubTrigger>
))
MenubarSubTrigger.displayName = MenubarPrimitive.SubTrigger.displayName

const MenubarSubContent = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.SubContent>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.SubContent>
>(({ className, ...props }, ref) => (
  <MenubarPrimitive.SubContent
    ref={ref}
    className={cn(
      "z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
      className,
    )}
    {...props}
  />
))
MenubarSubContent.displayName = MenubarPrimitive.SubContent.displayName

const MenubarContent = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Content>
>(
  (
    { className, align = "start", alignOffset = -4, sideOffset = 8, ...props },
    ref,
  ) => (
    <MenubarPrimitive.Portal>
      <MenubarPrimitive.Content
        ref={ref}
        align={align}
        alignOffset={alignOffset}
        sideOffset={sideOffset}
        className={cn(
          "z-50 min-w-[12rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
          className,
        )}
        {...props}
      />
    </MenubarPrimitive.Portal>
  ),
)
MenubarContent.displayName = MenubarPrimitive.Content.displayName

const MenubarItem = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Item> & {
    inset?: boolean
  }
>(({ className, inset, ...props }, ref) => (
  <MenubarPrimitive.Item
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      inset && "pl-8",
      className,
    )}
    {...props}
  />
))
MenubarItem.displayName = MenubarPrimitive.Item.displayName

const MenubarCheckboxItem = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.CheckboxItem>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.CheckboxItem>
>(({ className, children, checked, ...props }, ref) => (
  <MenubarPrimitive.CheckboxItem
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      className,
    )}
    checked={checked}
    {...props}
  >
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <MenubarPrimitive.ItemIndicator>
        <Check className="h-4 w-4" />
      </MenubarPrimitive.ItemIndicator>
    </span>
    {children}
  </MenubarPrimitive.CheckboxItem>
))
MenubarCheckboxItem.displayName = MenubarPrimitive.CheckboxItem.displayName

const MenubarRadioItem = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.RadioItem>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.RadioItem>
>(({ className, children, ...props }, ref) => (
  <MenubarPrimitive.RadioItem
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      className,
    )}
    {...props}
  >
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <MenubarPrimitive.ItemIndicator>
        <Circle className="h-2 w-2 fill-current" />
      </MenubarPrimitive.ItemIndicator>
    </span>
    {children}
  </MenubarPrimitive.RadioItem>
))
MenubarRadioItem.displayName = MenubarPrimitive.RadioItem.displayName

const MenubarLabel = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.Label>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Label> & {
    inset?: boolean
  }
>(({ className, inset, ...props }, ref) => (
  <MenubarPrimitive.Label
    ref={ref}
    className={cn(
      "px-2 py-1.5 text-sm font-semibold",
      inset && "pl-8",
      className,
    )}
    {...props}
  />
))
MenubarLabel.displayName = MenubarPrimitive.Label.displayName

const MenubarSeparator = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.Separator>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Separator>
>(({ className, ...props }, ref) => (
  <MenubarPrimitive.Separator
    ref={ref}
    className={cn("-mx-1 my-1 h-px bg-muted", className)}
    {...props}
  />
))
MenubarSeparator.displayName = MenubarPrimitive.Separator.displayName

const MenubarShortcut = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLSpanElement>) => {
  return (
    <span
      className={cn(
        "ml-auto text-xs tracking-widest text-muted-foreground",
        className,
      )}
      {...props}
    />
  )
}
MenubarShortcut.displayname = "MenubarShortcut"

export {
  Menubar,
  MenubarMenu,
  MenubarTrigger,
  MenubarContent,
  MenubarItem,
  MenubarSeparator,
  MenubarLabel,
  MenubarCheckboxItem,
  MenubarRadioGroup,
  MenubarRadioItem,
  MenubarPortal,
  MenubarSubContent,
  MenubarSubTrigger,
  MenubarGroup,
  MenubarSub,
  MenubarShortcut,
}

```

Install NPM dependencies:
```bash
lucide-react, @radix-ui/react-menubar
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

import {
  Menubar,
  MenubarContent,
  MenubarItem,
  MenubarMenu,
  MenubarSeparator,
  MenubarTrigger,
  MenubarSub,
  MenubarSubTrigger,
  MenubarSubContent,
} from "@/components/ui/menubar";
import {
  Folder,
  FolderPlus,
  FileText,
  Users,
  UserCheck,
  Settings,
  Bell,
  Calendar,
  ChevronRight,
  CheckCircle,
  Upload,
} from "lucide-react";

export default function AppMenuBar() {
  return (
    <Menubar className="bg-white border-b border-slate-200 shadow-sm rounded-b-lg">
      {/* Projects Menu */}
      <MenubarMenu>
        <MenubarTrigger className="flex items-center gap-2">
          <Folder className="w-4 h-4" />
          Projects
        </MenubarTrigger>
        <MenubarContent className="w-56">
          <MenubarItem className="flex items-center gap-2">
            <FolderPlus className="w-4 h-4" />
            New Project
          </MenubarItem>
          <MenubarItem className="flex items-center gap-2">
            <FileText className="w-4 h-4" />
            All Projects
          </MenubarItem>
          <MenubarItem className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4" />
            Completed Projects
          </MenubarItem>
        </MenubarContent>
      </MenubarMenu>

      {/* Teams Menu with Submenu */}
      <MenubarMenu>
        <MenubarTrigger className="flex items-center gap-2">
          <Users className="w-4 h-4" />
          Teams
        </MenubarTrigger>
        <MenubarContent className="w-56">
          <MenubarItem className="flex items-center gap-2">
            <UserCheck className="w-4 h-4" />
            All Members
          </MenubarItem>
          <MenubarItem className="flex items-center gap-2">
            <FolderPlus className="w-4 h-4" />
            Create Team
          </MenubarItem>

          <MenubarSeparator />

          {/* Proper Nested Submenu */}
          <MenubarSub>
            <MenubarSubTrigger className="flex items-center justify-between gap-2">
              Manage Teams
            </MenubarSubTrigger>
            <MenubarSubContent className="w-48">
              <MenubarItem className="flex items-center gap-2">
                <Settings className="w-4 h-4" />
                Team Settings
              </MenubarItem>
              <MenubarItem className="flex items-center gap-2">
                <Users className="w-4 h-4" />
                Team Members
              </MenubarItem>
            </MenubarSubContent>
          </MenubarSub>
        </MenubarContent>
      </MenubarMenu>

      {/* Calendar Menu */}
      <MenubarMenu>
        <MenubarTrigger className="flex items-center gap-2">
          <Calendar className="w-4 h-4" />
          Calendar
        </MenubarTrigger>
        <MenubarContent className="w-48">
          <MenubarItem className="flex items-center gap-2">
            <Calendar className="w-4 h-4" />
            View Calendar
          </MenubarItem>
          <MenubarItem className="flex items-center gap-2">
            <FileText className="w-4 h-4" />
            Schedule Task
          </MenubarItem>
        </MenubarContent>
      </MenubarMenu>

      {/* Notifications */}
      <MenubarMenu>
        <MenubarTrigger className="flex items-center gap-2">
          <Bell className="w-4 h-4" />
          Notifications
        </MenubarTrigger>
        <MenubarContent className="w-48">
          <MenubarItem className="flex items-center gap-2">
            <Bell className="w-4 h-4" />
            All Notifications
          </MenubarItem>
        </MenubarContent>
      </MenubarMenu>

      {/* Files Menu */}
      <MenubarMenu>
        <MenubarTrigger className="flex items-center gap-2">
          <Upload className="w-4 h-4" />
          Files
        </MenubarTrigger>
        <MenubarContent className="w-56">
          <MenubarItem className="flex items-center gap-2">
            <Upload className="w-4 h-4" />
            Upload File
          </MenubarItem>
          <MenubarItem className="flex items-center gap-2">
            <FileText className="w-4 h-4" />
            My Files
          </MenubarItem>
        </MenubarContent>
      </MenubarMenu>
    </Menubar>
  );
}
