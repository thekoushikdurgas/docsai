https://21st.dev/community/components/ravikatiyar/composer-input/default
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
composer-input.tsx
// components/ui/composer-input.tsx

import * as React from "react"
import { AnimatePresence, motion } from "framer-motion"
import {
  Bold,
  Italic,
  Underline,
  List,
  ListOrdered,
  Quote,
  Code,
  Link,
  Trash2,
  Paperclip,
  Mic,
  Image as ImageIcon,
  Wand2,
  MoreHorizontal,
  CornerDownLeft,
  X,
} from "lucide-react"

import { cn } from "@/lib/utils" // Your utility for merging class names
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"

// Define the structure for an attachment
export interface Attachment {
  id: string
  fileName: string
  fileType: "image" | "document"
  thumbnailUrl?: string // URL for image previews
}

// Define props for the component
export interface ComposerInputProps extends React.HTMLAttributes<HTMLDivElement> {
  onSend: (message: string, attachments: Attachment[]) => void
  initialAttachments?: Attachment[]
  placeholder?: string
}

const ComposerInput = React.forwardRef<HTMLDivElement, ComposerInputProps>(
  ({ className, onSend, initialAttachments = [], placeholder = "Type your message...", ...props }, ref) => {
    const [message, setMessage] = React.useState("")
    const [attachments, setAttachments] = React.useState<Attachment[]>(initialAttachments)

    const handleSend = () => {
      if (message.trim() || attachments.length > 0) {
        onSend(message, attachments)
        setMessage("")
        setAttachments([])
      }
    }

    const handleRemoveAttachment = (id: string) => {
      setAttachments((prev) => prev.filter((att) => att.id !== id))
    }
    
    // An array of toolbar items for easier mapping
    const toolbarItems = [
      { icon: Bold, tooltip: "Bold" },
      { icon: Italic, tooltip: "Italic" },
      { icon: Underline, tooltip: "Underline" },
      { icon: List, tooltip: "Bullet List" },
      { icon: ListOrdered, tooltip: "Numbered List" },
      { icon: Quote, tooltip: "Quote" },
      { icon: Code, tooltip: "Code" },
      { icon: Link, tooltip: "Link" },
    ];
    
    // An array of action button items
    const actionItems = [
      { icon: Paperclip, tooltip: "Attach File" },
      { icon: Mic, tooltip: "Voice Message" },
      { icon: ImageIcon, tooltip: "Add Image" },
      { icon: Wand2, tooltip: "AI Assist" },
      { icon: MoreHorizontal, tooltip: "More Options" },
    ];

    return (
      <TooltipProvider>
        <div
          ref={ref}
          className={cn(
            "flex flex-col w-full rounded-xl border bg-card text-card-foreground shadow-sm transition-all duration-300 ease-in-out focus-within:ring-2 focus-within:ring-ring focus-within:ring-offset-2 focus-within:ring-offset-background",
            className
          )}
          {...props}
        >
          {/* Top Toolbar */}
          <div className="flex items-center justify-between p-2 border-b">
            <div className="flex items-center gap-1">
              {toolbarItems.map((item, index) => (
                <Tooltip key={index}>
                  <TooltipTrigger asChild>
                    <Button variant="ghost" size="icon" className="h-8 w-8">
                      <item.icon className="h-4 w-4" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>{item.tooltip}</p>
                  </TooltipContent>
                </Tooltip>
              ))}
            </div>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost" size="icon" className="h-8 w-8 text-destructive">
                  <Trash2 className="h-4 w-4" />
                </Button>
              </TooltipTrigger>
              <TooltipContent>
                <p>Clear</p>
              </TooltipContent>
            </Tooltip>
          </div>

          {/* Main text area */}
          <div className="p-2 flex-grow">
            <Textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder={placeholder}
              className="w-full min-h-[100px] border-0 resize-none focus-visible:ring-0 focus-visible:ring-offset-0 p-2"
            />
          </div>

          {/* Attachments Preview */}
          {attachments.length > 0 && (
            <div className="px-4 pb-2">
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
                <AnimatePresence>
                  {attachments.map((att) => (
                    <motion.div
                      key={att.id}
                      layout
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.8 }}
                      transition={{ type: "spring", stiffness: 300, damping: 30 }}
                      className="relative group"
                    >
                      <div className="aspect-square w-full rounded-md overflow-hidden bg-muted flex items-center justify-center">
                        {att.fileType === "image" && att.thumbnailUrl ? (
                          <img src={att.thumbnailUrl} alt={att.fileName} className="h-full w-full object-cover"/>
                        ) : (
                          <Paperclip className="h-6 w-6 text-muted-foreground" />
                        )}
                      </div>
                       <button
                          onClick={() => handleRemoveAttachment(att.id)}
                          className="absolute -top-1 -right-1 bg-background border rounded-full p-0.5 text-destructive opacity-0 group-hover:opacity-100 transition-opacity"
                          aria-label="Remove attachment"
                        >
                          <X className="h-3 w-3" />
                        </button>
                    </motion.div>
                  ))}
                </AnimatePresence>
              </div>
            </div>
          )}

          {/* Bottom Action Bar */}
          <div className="flex items-center justify-between p-2 border-t">
            <div className="flex items-center gap-1">
              {actionItems.map((item, index) => (
                 <Tooltip key={index}>
                  <TooltipTrigger asChild>
                    <Button variant="ghost" size="icon" className="h-8 w-8">
                      <item.icon className="h-4 w-4" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>{item.tooltip}</p>
                  </TooltipContent>
                </Tooltip>
              ))}
            </div>
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Button onClick={handleSend} size="sm">
                Send
                <CornerDownLeft className="h-4 w-4 ml-2" />
              </Button>
            </motion.div>
          </div>
        </div>
      </TooltipProvider>
    )
  }
)

ComposerInput.displayName = "ComposerInput"

export { ComposerInput }

demo.tsx
// demo.tsx

import React from "react"
import { toast } from "sonner"
import { ComposerInput, Attachment } from "@/components/ui/composer-input" // Adjust path as needed

// Sample attachments for the demo
const sampleAttachments: Attachment[] = [
  {
    id: '1',
    fileName: 'Project-Brief.pdf',
    fileType: 'document',
  },
  {
    id: '2',
    fileName: 'UI-Mockup.png',
    fileType: 'image',
    thumbnailUrl: 'https://images.unsplash.com/photo-1543286386-713bdd548da4?w=200',
  },
  {
    id: '3',
    fileName: 'Design-Assets.zip',
    fileType: 'document',
  }
];

export default function ComposerInputDemo() {
  const handleSend = (message: string, attachments: Attachment[]) => {
    // In a real app, this function would send the data to an API
    console.log("Sending message:", message)
    console.log("With attachments:", attachments)

    // Use sonner to show a success toast
    toast.success("Message Sent!", {
      description: `Your message and ${attachments.length} attachments have been sent.`,
      duration: 3000,
    })
  }

  return (
    <div className="w-full max-w-2xl mx-auto p-4 flex flex-col items-center justify-center min-h-[400px]">
      <h2 className="text-2xl font-bold mb-4">Leave a Comment</h2>
      <ComposerInput
        onSend={handleSend}
        initialAttachments={sampleAttachments}
        placeholder="Share your thoughts or attach a file..."
        aria-label="Comment composer"
      />
    </div>
  )
}
```

Copy-paste these files for dependencies:
```tsx
arunachalam0606/toast
'use client'

import { forwardRef, useImperativeHandle, useRef } from 'react';
import { motion } from 'framer-motion';
import {
  Toaster as SonnerToaster,
  toast as sonnerToast,
} from 'sonner';
import {
  CheckCircle,
  AlertCircle,
  Info,
  AlertTriangle,
  X,
} from 'lucide-react';

import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

type Variant = 'default' | 'success' | 'error' | 'warning';
type Position =
  | 'top-left'
  | 'top-center'
  | 'top-right'
  | 'bottom-left'
  | 'bottom-center'
  | 'bottom-right';

interface ActionButton {
  label: string;
  onClick: () => void;
  variant?: 'default' | 'outline' | 'ghost';
}

interface ToasterProps {
  title?: string;
  message: string;
  variant?: Variant;
  duration?: number;
  position?: Position;
  actions?: ActionButton;
  onDismiss?: () => void;
  highlightTitle?: boolean;
}

export interface ToasterRef {
  show: (props: ToasterProps) => void;
}

const variantStyles: Record<Variant, string> = {
  default: 'bg-card border-border text-foreground',
  success: 'bg-card border-green-600/50',
  error: 'bg-card border-destructive/50',
  warning: 'bg-card border-amber-600/50',
};

const titleColor: Record<Variant, string> = {
  default: 'text-foreground',
  success: 'text-green-600 dark:text-green-400',
  error: 'text-destructive',
  warning: 'text-amber-600 dark:text-amber-400',
};

const iconColor: Record<Variant, string> = {
  default: 'text-muted-foreground',
  success: 'text-green-600 dark:text-green-400',
  error: 'text-destructive',
  warning: 'text-amber-600 dark:text-amber-400',
};

const variantIcons: Record<Variant, React.ComponentType<{ className?: string }>> = {
  default: Info,
  success: CheckCircle,
  error: AlertCircle,
  warning: AlertTriangle,
};

const toastAnimation = {
  initial: { opacity: 0, y: 50, scale: 0.95 },
  animate: { opacity: 1, y: 0, scale: 1 },
  exit: { opacity: 0, y: 50, scale: 0.95 },
};

const Toaster = forwardRef<ToasterRef, { defaultPosition?: Position }>(
  ({ defaultPosition = 'bottom-right' }, ref) => {
    const toastReference = useRef<ReturnType<typeof sonnerToast.custom> | null>(null);

    useImperativeHandle(ref, () => ({
      show({
        title,
        message,
        variant = 'default',
        duration = 4000,
        position = defaultPosition,
        actions,
        onDismiss,
        highlightTitle,
      }) {
        const Icon = variantIcons[variant];

        toastReference.current = sonnerToast.custom(
          (toastId) => (
            <motion.div
              variants={toastAnimation}
              initial="initial"
              animate="animate"
              exit="exit"
              transition={{ duration: 0.3, ease: 'easeOut' }}
              className={cn(
                'flex items-center justify-between w-full max-w-xs p-3 rounded-xl border shadow-md',
                variantStyles[variant]
              )}
            >
              <div className="flex items-start gap-2">
                <Icon className={cn('h-4 w-4 mt-0.5 flex-shrink-0', iconColor[variant])} />
                <div className="space-y-0.5">
                  {title && (
                    <h3
                      className={cn(
                        'text-xs font-medium leading-none',
                        titleColor[variant],
                        highlightTitle && titleColor['success'] // override for meeting case
                      )}
                    >
                      {title}
                    </h3>
                  )}
                  <p className="text-xs text-muted-foreground">{message}</p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                {actions?.label && (
                  <Button
                    variant={actions.variant || 'outline'}
                    size="sm"
                    onClick={() => {
                      actions.onClick();
                      sonnerToast.dismiss(toastId);
                    }}
                    className={cn(
                      'cursor-pointer',
                      variant === 'success'
                        ? 'text-green-600 border-green-600 hover:bg-green-600/10 dark:hover:bg-green-400/20'
                        : variant === 'error'
                        ? 'text-destructive border-destructive hover:bg-destructive/10 dark:hover:bg-destructive/20'
                        : variant === 'warning'
                        ? 'text-amber-600 border-amber-600 hover:bg-amber-600/10 dark:hover:bg-amber-400/20'
                        : 'text-foreground border-border hover:bg-muted/10 dark:hover:bg-muted/20'
                    )}
                  >
                    {actions.label}
                  </Button>
                )}

                <button
                  onClick={() => {
                    sonnerToast.dismiss(toastId);
                    onDismiss?.();
                  }}
                  className="rounded-full p-1 hover:bg-muted/50 dark:hover:bg-muted/30 transition-colors focus:outline-none focus:ring-2 focus:ring-ring"
                  aria-label="Dismiss notification"
                >
                  <X className="h-3 w-3 text-muted-foreground" />
                </button>
              </div>
            </motion.div>
          ),
          { duration, position }
        );
      },
    }));

    return (
      <SonnerToaster
        position={defaultPosition}
        toastOptions={{ unstyled: true, className: 'flex justify-end' }}
      />
    );
  }
);

export default Toaster;

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
shadcn/textarea
import * as React from "react"

import { cn } from "@/lib/utils"

export interface TextareaProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, ...props }, ref) => {
    return (
      <textarea
        className={cn(
          "flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Textarea.displayName = "Textarea"

export { Textarea }

```
```tsx
originui/tooltip
"use client";

import * as TooltipPrimitive from "@radix-ui/react-tooltip";
import * as React from "react";

import { cn } from "@/lib/utils";

const TooltipProvider = TooltipPrimitive.Provider;

const Tooltip = TooltipPrimitive.Root;

const TooltipTrigger = TooltipPrimitive.Trigger;

const TooltipContent = React.forwardRef<
  React.ElementRef<typeof TooltipPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof TooltipPrimitive.Content> & {
    showArrow?: boolean;
  }
>(({ className, sideOffset = 4, showArrow = false, ...props }, ref) => (
  <TooltipPrimitive.Portal>
    <TooltipPrimitive.Content
      ref={ref}
      sideOffset={sideOffset}
      className={cn(
        "relative z-50 max-w-[280px] rounded-lg border border-border bg-popover px-3 py-1.5 text-sm text-popover-foreground animate-in fade-in-0 zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
        className,
      )}
      {...props}
    >
      {props.children}
      {showArrow && (
        <TooltipPrimitive.Arrow className="-my-px fill-popover drop-shadow-[0_1px_0_hsl(var(--border))]" />
      )}
    </TooltipPrimitive.Content>
  </TooltipPrimitive.Portal>
));
TooltipContent.displayName = TooltipPrimitive.Content.displayName;

export { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger };

```
```tsx
ravikatiyar162/download-toast
import React, { useState, useEffect } from 'react';

// --- Helper Components ---

// Animated Grid Background
const GridBackground = () => (
    <div className="absolute inset-0 z-0 overflow-hidden">
        <div 
            className="absolute inset-[-10%] animate-grid-pan"
            style={{
                backgroundImage: 'linear-gradient(to right, #80808012 1px, transparent 1px), linear-gradient(to bottom, #80808012 1px, transparent 1px)',
                backgroundSize: '24px 24px',
                maskImage: 'radial-gradient(ellipse 50% 50% at 50% 50%, #000 60%, transparent 100%)',
            }}
        ></div>
        <style>
        {`
            @keyframes grid-pan {
                0% { transform: translate(0, 0); }
                100% { transform: translate(24px, 24px); }
            }
            .animate-grid-pan {
                animation: grid-pan 10s linear infinite;
            }
        `}
        </style>
    </div>
);


// Theme Toggle Switch
const ThemeToggle = ({ darkMode, setDarkMode }) => (
  <button
    onClick={() => setDarkMode(!darkMode)}
    className="absolute top-6 right-6 z-20 p-2 rounded-full text-gray-500 dark:text-gray-400 bg-gray-200/50 dark:bg-gray-700/50 hover:bg-gray-300/70 dark:hover:bg-gray-600/70 transition-all duration-300"
    aria-label="Toggle theme"
  >
    {darkMode ? (
       // Sun Icon
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="5"></circle>
        <line x1="12" y1="1" x2="12" y2="3"></line>
        <line x1="12" y1="21" x2="12" y2="23"></line>
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
        <line x1="1" y1="12" x2="3" y2="12"></line>
        <line x1="21" y1="12" x2="23" y2="12"></line>
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
      </svg>
    ) : (
      // Moon Icon
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
      </svg>
    )}
  </button>
);

// Icon for the file type, now with a universal folded corner
const FileIcon = ({ type }) => {
  const typeStyles = {
    PDF: { bg: 'bg-red-500', text: '.PDF' },
    XLS: { bg: 'bg-green-500', text: '.XLS' },
    DOCX: { bg: 'bg-blue-500', text: '.DOC' },
  };

  const style = typeStyles[type] || { bg: 'bg-gray-500', text: 'FILE' };

  return (
    <div className={`relative flex-shrink-0 w-14 h-14 ${style.bg} rounded-lg flex items-center justify-center mr-4 overflow-hidden`}>
      {/* This creates the folded corner effect for all icons */}
      <div
        className="absolute top-0 right-0 w-4 h-4 bg-slate-50 dark:bg-slate-900 transition-colors duration-300"
        style={{ clipPath: 'polygon(100% 0, 0 0, 100% 100%)' }}
      ></div>
      <span className="text-white font-bold text-sm">{style.text}</span>
    </div>
  );
};


// Progress bar for downloading items
const ProgressBar = ({ progress }) => (
  <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1.5 mt-1.5">
    <div
      className="bg-blue-500 h-1.5 rounded-full transition-all duration-500 ease-out"
      style={{ width: `${progress}%` }}
    ></div>
  </div>
);

// Action buttons (Download/Cancel)
const ActionButton = ({ status, onCancel }) => {
  if (status === 'downloading') {
    return (
      <button onClick={onCancel} className="text-slate-500 dark:text-slate-400 font-semibold text-sm hover:text-slate-800 dark:hover:text-slate-200 transition-colors duration-200">
        Cancel
      </button>
    );
  }
  return (
    <button className="text-blue-600 dark:text-blue-500 font-semibold text-sm hover:text-blue-800 dark:hover:text-blue-400 transition-colors duration-200">
      Download
    </button>
  );
};

// --- Main File Item Component (Now fully responsive) ---
const FileItem = ({ file, onCancel }) => {
  const { name, type, subtype, size, status, progress } = file;
  const displaySize = size < 1 ? `${(size * 1000).toFixed(0)} KB` : `${size} MB`;

  return (
    <div className="flex flex-wrap items-center py-3">
      {/* Container for Icon and Name/Progress */}
      <div className="flex items-center flex-grow min-w-0">
        <FileIcon type={type} />
        <div className="flex-grow min-w-0">
          <p className="font-semibold text-slate-800 dark:text-slate-200 truncate">{name}</p>
          {status === 'downloading' ? (
            <ProgressBar progress={progress} />
          ) : (
            <p className="text-sm text-slate-500 dark:text-slate-400">{subtype}</p>
          )}
        </div>
      </div>
      
      {/* Container for Size and Button, wraps on mobile */}
      <div className="flex items-center justify-end w-full sm:w-auto mt-2 sm:mt-0 pl-[72px] sm:pl-0">
        <div className="flex-shrink-0 w-20 text-right text-sm font-medium text-slate-500 dark:text-slate-400">
          {displaySize}
        </div>
        <div className="flex-shrink-0 w-24 text-right">
          <ActionButton status={status} onCancel={() => onCancel(file.id)} />
        </div>
      </div>
    </div>
  );
};

// --- App Component ---
export default function App() {
  // Respect user's system preference for dark mode
  const [darkMode, setDarkMode] = useState(
    () => window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
  );

  const initialFiles = [
    { id: 1, name: 'ReactJS-for-beginner.pdf', type: 'PDF', size: 4.5, status: 'downloading', progress: 0, originalSubtype: 'Portable Document Format', subtype: 'Downloading...' },
    { id: 2, name: 'Database-MySQL.xls', type: 'XLS', size: 25.7, status: 'complete', progress: 100, subtype: 'Microsoft Excel' },
    { id: 3, name: 'Summary-of-php.docx', type: 'DOCX', size: 0.35, status: 'complete', progress: 100, subtype: 'Microsoft Word' },
  ];
  const [files, setFiles] = useState(initialFiles);

  // Effect for download simulation
  useEffect(() => {
    const interval = setInterval(() => {
      setFiles(currentFiles =>
        currentFiles.map(file => {
          if (file.status === 'downloading' && file.progress < 100) {
            const increment = Math.random() * 8;
            const newProgress = Math.min(file.progress + increment, 100);
            if (newProgress >= 100) {
              return { ...file, progress: 100, status: 'complete', subtype: file.originalSubtype };
            }
            return { ...file, progress: newProgress };
          }
          return file;
        })
      );
    }, 200);
    return () => clearInterval(interval);
  }, []);

  // Effect to update the class on the root <html> element
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const handleCancel = (fileId) => {
    setFiles(currentFiles =>
      currentFiles.map(file =>
        file.id === fileId ? { ...file, status: 'complete', progress: 100, subtype: 'Cancelled' } : file
      )
    );
  };

  return (
    <div className="relative bg-slate-50 dark:bg-slate-900 min-h-screen w-full flex items-center justify-center font-sans transition-colors duration-300 py-8">
      <GridBackground />
      <ThemeToggle darkMode={darkMode} setDarkMode={setDarkMode} />
      <div className="relative w-full max-w-lg mx-4 sm:mx-auto bg-white/70 dark:bg-slate-800/70 backdrop-blur-xl rounded-2xl shadow-lg border border-slate-200 dark:border-slate-700 p-4 sm:p-8">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-4 px-2 sm:px-0">Your Downloads</h1>
        <div>
          {files.map(file => (
            <FileItem key={file.id} file={file} onCancel={handleCancel} />
          ))}
        </div>
      </div>
    </div>
  );
}

```

Install NPM dependencies:
```bash
lucide-react, framer-motion, sonner, @radix-ui/react-slot, class-variance-authority, @radix-ui/react-tooltip
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
// components/ui/composer-input.tsx

import * as React from "react"
import { AnimatePresence, motion } from "framer-motion"
import {
  Bold,
  Italic,
  Underline,
  List,
  ListOrdered,
  Quote,
  Code,
  Link,
  Trash2,
  Paperclip,
  Mic,
  Image as ImageIcon,
  Wand2,
  MoreHorizontal,
  CornerDownLeft,
  X,
} from "lucide-react"

import { cn } from "@/lib/utils" // Your utility for merging class names
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"

// Define the structure for an attachment
export interface Attachment {
  id: string
  fileName: string
  fileType: "image" | "document"
  thumbnailUrl?: string // URL for image previews
}

// Define props for the component
export interface ComposerInputProps extends React.HTMLAttributes<HTMLDivElement> {
  onSend: (message: string, attachments: Attachment[]) => void
  initialAttachments?: Attachment[]
  placeholder?: string
}

const ComposerInput = React.forwardRef<HTMLDivElement, ComposerInputProps>(
  ({ className, onSend, initialAttachments = [], placeholder = "Type your message...", ...props }, ref) => {
    const [message, setMessage] = React.useState("")
    const [attachments, setAttachments] = React.useState<Attachment[]>(initialAttachments)

    const handleSend = () => {
      if (message.trim() || attachments.length > 0) {
        onSend(message, attachments)
        setMessage("")
        setAttachments([])
      }
    }

    const handleRemoveAttachment = (id: string) => {
      setAttachments((prev) => prev.filter((att) => att.id !== id))
    }
    
    // An array of toolbar items for easier mapping
    const toolbarItems = [
      { icon: Bold, tooltip: "Bold" },
      { icon: Italic, tooltip: "Italic" },
      { icon: Underline, tooltip: "Underline" },
      { icon: List, tooltip: "Bullet List" },
      { icon: ListOrdered, tooltip: "Numbered List" },
      { icon: Quote, tooltip: "Quote" },
      { icon: Code, tooltip: "Code" },
      { icon: Link, tooltip: "Link" },
    ];
    
    // An array of action button items
    const actionItems = [
      { icon: Paperclip, tooltip: "Attach File" },
      { icon: Mic, tooltip: "Voice Message" },
      { icon: ImageIcon, tooltip: "Add Image" },
      { icon: Wand2, tooltip: "AI Assist" },
      { icon: MoreHorizontal, tooltip: "More Options" },
    ];

    return (
      <TooltipProvider>
        <div
          ref={ref}
          className={cn(
            "flex flex-col w-full rounded-xl border bg-card text-card-foreground shadow-sm transition-all duration-300 ease-in-out focus-within:ring-2 focus-within:ring-ring focus-within:ring-offset-2 focus-within:ring-offset-background",
            className
          )}
          {...props}
        >
          {/* Top Toolbar */}
          <div className="flex items-center justify-between p-2 border-b">
            <div className="flex items-center gap-1">
              {toolbarItems.map((item, index) => (
                <Tooltip key={index}>
                  <TooltipTrigger asChild>
                    <Button variant="ghost" size="icon" className="h-8 w-8">
                      <item.icon className="h-4 w-4" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>{item.tooltip}</p>
                  </TooltipContent>
                </Tooltip>
              ))}
            </div>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost" size="icon" className="h-8 w-8 text-destructive">
                  <Trash2 className="h-4 w-4" />
                </Button>
              </TooltipTrigger>
              <TooltipContent>
                <p>Clear</p>
              </TooltipContent>
            </Tooltip>
          </div>

          {/* Main text area */}
          <div className="p-2 flex-grow">
            <Textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder={placeholder}
              className="w-full min-h-[100px] border-0 resize-none focus-visible:ring-0 focus-visible:ring-offset-0 p-2"
            />
          </div>

          {/* Attachments Preview */}
          {attachments.length > 0 && (
            <div className="px-4 pb-2">
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
                <AnimatePresence>
                  {attachments.map((att) => (
                    <motion.div
                      key={att.id}
                      layout
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.8 }}
                      transition={{ type: "spring", stiffness: 300, damping: 30 }}
                      className="relative group"
                    >
                      <div className="aspect-square w-full rounded-md overflow-hidden bg-muted flex items-center justify-center">
                        {att.fileType === "image" && att.thumbnailUrl ? (
                          <img src={att.thumbnailUrl} alt={att.fileName} className="h-full w-full object-cover"/>
                        ) : (
                          <Paperclip className="h-6 w-6 text-muted-foreground" />
                        )}
                      </div>
                       <button
                          onClick={() => handleRemoveAttachment(att.id)}
                          className="absolute -top-1 -right-1 bg-background border rounded-full p-0.5 text-destructive opacity-0 group-hover:opacity-100 transition-opacity"
                          aria-label="Remove attachment"
                        >
                          <X className="h-3 w-3" />
                        </button>
                    </motion.div>
                  ))}
                </AnimatePresence>
              </div>
            </div>
          )}

          {/* Bottom Action Bar */}
          <div className="flex items-center justify-between p-2 border-t">
            <div className="flex items-center gap-1">
              {actionItems.map((item, index) => (
                 <Tooltip key={index}>
                  <TooltipTrigger asChild>
                    <Button variant="ghost" size="icon" className="h-8 w-8">
                      <item.icon className="h-4 w-4" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>{item.tooltip}</p>
                  </TooltipContent>
                </Tooltip>
              ))}
            </div>
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Button onClick={handleSend} size="sm">
                Send
                <CornerDownLeft className="h-4 w-4 ml-2" />
              </Button>
            </motion.div>
          </div>
        </div>
      </TooltipProvider>
    )
  }
)

ComposerInput.displayName = "ComposerInput"

export { ComposerInput }
https://21st.dev/community/components/originui/dialog/rating-dialog
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
dialog.tsx
"use client";

import * as DialogPrimitive from "@radix-ui/react-dialog";
import * as React from "react";

import { cn } from "@/lib/utils";
import { Cross2Icon } from "@radix-ui/react-icons";

const Dialog = DialogPrimitive.Root;

const DialogTrigger = DialogPrimitive.Trigger;

const DialogPortal = DialogPrimitive.Portal;

const DialogClose = DialogPrimitive.Close;

const DialogOverlay = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn(
      "fixed inset-0 z-[101] bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
      className,
    )}
    {...props}
  />
));
DialogOverlay.displayName = DialogPrimitive.Overlay.displayName;

const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DialogPortal>
    <DialogOverlay />
    <DialogPrimitive.Content
      ref={ref}
      className={cn(
        "fixed left-1/2 top-1/2 z-[101] grid max-h-[calc(100%-4rem)] w-full -translate-x-1/2 -translate-y-1/2 gap-4 overflow-y-auto border bg-background p-6 shadow-lg shadow-black/5 duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:max-w-[400px] sm:rounded-xl",
        className,
      )}
      {...props}
    >
      {children}
      <DialogPrimitive.Close className="group absolute right-3 top-3 flex size-7 items-center justify-center rounded-lg outline-offset-2 transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring/70 disabled:pointer-events-none">
        <Cross2Icon
          width={16}
          height={16}
          strokeWidth={2}
          className="opacity-60 transition-opacity group-hover:opacity-100"
        />
        <span className="sr-only">Close</span>
      </DialogPrimitive.Close>
    </DialogPrimitive.Content>
  </DialogPortal>
));
DialogContent.displayName = DialogPrimitive.Content.displayName;

const DialogHeader = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("flex flex-col space-y-1.5 text-center sm:text-left", className)} {...props} />
);
DialogHeader.displayName = "DialogHeader";

const DialogFooter = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn("flex flex-col-reverse gap-2 sm:flex-row sm:justify-end sm:gap-3", className)}
    {...props}
  />
);
DialogFooter.displayName = "DialogFooter";

const DialogTitle = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Title>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Title
    ref={ref}
    className={cn("text-lg font-semibold tracking-tight", className)}
    {...props}
  />
));
DialogTitle.displayName = DialogPrimitive.Title.displayName;

const DialogDescription = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Description>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Description
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
));
DialogDescription.displayName = DialogPrimitive.Description.displayName;

export {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogOverlay,
  DialogPortal,
  DialogTitle,
  DialogTrigger,
};


demo.tsx
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Textarea } from "@/components/ui/textarea";

function Component() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">Rating</Button>
      </DialogTrigger>
      <DialogContent className="flex flex-col gap-0 p-0 [&>button:last-child]:top-3.5">
        <DialogHeader className="contents space-y-0 text-left">
          <DialogTitle className="border-b border-border px-6 py-4 text-base">
            Help us improve
          </DialogTitle>
        </DialogHeader>
        <div className="px-6 py-4">
          <form className="space-y-5">
            <div className="space-y-4">
              <div>
                <fieldset className="space-y-4">
                  <legend className="text-lg font-semibold leading-none text-foreground">
                    How hard was it to set up your account?
                  </legend>
                  <RadioGroup className="flex gap-0 -space-x-px rounded-lg shadow-sm shadow-black/5">
                    {[0, 1, 2, 3, 4, 5, 6, 7, 8].map((number) => (
                      <label
                        key={number}
                        className="relative flex size-9 flex-1 cursor-pointer flex-col items-center justify-center gap-3 border border-input text-center text-sm outline-offset-2 transition-colors first:rounded-s-lg last:rounded-e-lg has-[[data-state=checked]]:z-10 has-[[data-disabled]]:cursor-not-allowed has-[[data-state=checked]]:border-ring has-[[data-state=checked]]:bg-accent has-[[data-disabled]]:opacity-50 has-[:focus-visible]:outline has-[:focus-visible]:outline-2 has-[:focus-visible]:outline-ring/70"
                      >
                        <RadioGroupItem
                          id={`radio-17-r${number}`}
                          value={number.toString()}
                          className="sr-only after:absolute after:inset-0"
                        />
                        {number}
                      </label>
                    ))}
                  </RadioGroup>
                </fieldset>
                <div className="mt-2 flex justify-between text-xs text-muted-foreground">
                  <p>Very easy</p>
                  <p>Very dificult</p>
                </div>
              </div>

              <div className="space-y-2">
                <Label>Why did you give this rating?</Label>
                <Textarea
                  id="feedback"
                  placeholder="How can we improve Origin UI?"
                  aria-label="Send feedback"
                />
              </div>
            </div>
            <Button type="button" className="w-full">
              Send feedback
            </Button>
          </form>
        </div>
      </DialogContent>
    </Dialog>
  );
}

export { Component };

```

Copy-paste these files for dependencies:
```tsx
originui/button
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import * as React from "react";

import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-lg text-sm font-medium transition-colors outline-offset-2 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring/70 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground shadow-sm shadow-black/5 hover:bg-primary/90",
        destructive:
          "bg-destructive text-destructive-foreground shadow-sm shadow-black/5 hover:bg-destructive/90",
        outline:
          "border border-input bg-background shadow-sm shadow-black/5 hover:bg-accent hover:text-accent-foreground",
        secondary:
          "bg-secondary text-secondary-foreground shadow-sm shadow-black/5 hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-lg px-3 text-xs",
        lg: "h-10 rounded-lg px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />
    );
  },
);
Button.displayName = "Button";

export { Button, buttonVariants };

```
```tsx
originui/label
"use client";

import * as React from "react";

import { cn } from "@/lib/utils";

const Label = React.forwardRef<HTMLLabelElement, React.LabelHTMLAttributes<HTMLLabelElement>>(
  ({ className, ...props }, ref) => (
    <label
      ref={ref}
      className={cn(
        "text-sm font-medium leading-4 text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
        className,
      )}
      {...props}
    />
  ),
);
Label.displayName = "Label";

export { Label };

```
```tsx
shadcn/radio-group
"use client"

import * as React from "react"
import * as RadioGroupPrimitive from "@radix-ui/react-radio-group"
import { Circle } from "lucide-react"

import { cn } from "@/lib/utils"

const RadioGroup = React.forwardRef<
  React.ElementRef<typeof RadioGroupPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof RadioGroupPrimitive.Root>
>(({ className, ...props }, ref) => {
  return (
    <RadioGroupPrimitive.Root
      className={cn("grid gap-2", className)}
      {...props}
      ref={ref}
    />
  )
})
RadioGroup.displayName = RadioGroupPrimitive.Root.displayName

const RadioGroupItem = React.forwardRef<
  React.ElementRef<typeof RadioGroupPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof RadioGroupPrimitive.Item>
>(({ className, ...props }, ref) => {
  return (
    <RadioGroupPrimitive.Item
      ref={ref}
      className={cn(
        "aspect-square h-4 w-4 rounded-full border border-primary text-primary ring-offset-background focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
        className,
      )}
      {...props}
    >
      <RadioGroupPrimitive.Indicator className="flex items-center justify-center">
        <Circle className="h-2.5 w-2.5 fill-current text-current" />
      </RadioGroupPrimitive.Indicator>
    </RadioGroupPrimitive.Item>
  )
})
RadioGroupItem.displayName = RadioGroupPrimitive.Item.displayName

export { RadioGroup, RadioGroupItem }

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
originui/textarea
import * as React from "react";

import { cn } from "@/lib/utils";

const Textarea = React.forwardRef<HTMLTextAreaElement, React.ComponentProps<"textarea">>(
  ({ className, ...props }, ref) => {
    return (
      <textarea
        className={cn(
          "flex min-h-[80px] w-full rounded-lg border border-input bg-background px-3 py-2 text-sm text-foreground shadow-sm shadow-black/5 transition-shadow placeholder:text-muted-foreground/70 focus-visible:border-ring focus-visible:outline-none focus-visible:ring-[3px] focus-visible:ring-ring/20 disabled:cursor-not-allowed disabled:opacity-50",
          className,
        )}
        ref={ref}
        {...props}
      />
    );
  },
);
Textarea.displayName = "Textarea";

export { Textarea };

```

Install NPM dependencies:
```bash
@radix-ui/react-icons, @radix-ui/react-dialog, @radix-ui/react-slot, class-variance-authority, lucide-react, @radix-ui/react-radio-group, @radix-ui/react-label
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

import * as DialogPrimitive from "@radix-ui/react-dialog";
import * as React from "react";

import { cn } from "@/lib/utils";
import { Cross2Icon } from "@radix-ui/react-icons";

const Dialog = DialogPrimitive.Root;

const DialogTrigger = DialogPrimitive.Trigger;

const DialogPortal = DialogPrimitive.Portal;

const DialogClose = DialogPrimitive.Close;

const DialogOverlay = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn(
      "fixed inset-0 z-[101] bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
      className,
    )}
    {...props}
  />
));
DialogOverlay.displayName = DialogPrimitive.Overlay.displayName;

const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DialogPortal>
    <DialogOverlay />
    <DialogPrimitive.Content
      ref={ref}
      className={cn(
        "fixed left-1/2 top-1/2 z-[101] grid max-h-[calc(100%-4rem)] w-full -translate-x-1/2 -translate-y-1/2 gap-4 overflow-y-auto border bg-background p-6 shadow-lg shadow-black/5 duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:max-w-[400px] sm:rounded-xl",
        className,
      )}
      {...props}
    >
      {children}
      <DialogPrimitive.Close className="group absolute right-3 top-3 flex size-7 items-center justify-center rounded-lg outline-offset-2 transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring/70 disabled:pointer-events-none">
        <Cross2Icon
          width={16}
          height={16}
          strokeWidth={2}
          className="opacity-60 transition-opacity group-hover:opacity-100"
        />
        <span className="sr-only">Close</span>
      </DialogPrimitive.Close>
    </DialogPrimitive.Content>
  </DialogPortal>
));
DialogContent.displayName = DialogPrimitive.Content.displayName;

const DialogHeader = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("flex flex-col space-y-1.5 text-center sm:text-left", className)} {...props} />
);
DialogHeader.displayName = "DialogHeader";

const DialogFooter = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn("flex flex-col-reverse gap-2 sm:flex-row sm:justify-end sm:gap-3", className)}
    {...props}
  />
);
DialogFooter.displayName = "DialogFooter";

const DialogTitle = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Title>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Title
    ref={ref}
    className={cn("text-lg font-semibold tracking-tight", className)}
    {...props}
  />
));
DialogTitle.displayName = DialogPrimitive.Title.displayName;

const DialogDescription = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Description>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Description
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
));
DialogDescription.displayName = DialogPrimitive.Description.displayName;

export {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogOverlay,
  DialogPortal,
  DialogTitle,
  DialogTrigger,
};
