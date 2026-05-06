https://21st.dev/community/components/shugar/feedback/inline
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
feedback.tsx
import React, { useEffect, useRef, useState } from "react";
import { Button } from "@/components/ui/button-1";
import { Material } from "@/components/ui/material-1";
import { Textarea } from "@/components/ui/textarea";
import clsx from "clsx";
import { useClickOutside } from "@/components/ui/use-click-outside";

interface FeedbackProps {
  label: string;
  type?: "default" | "inline";
}

const MSupportedIcon = () => (
  <svg
    fill="none"
    height="14"
    viewBox="0 0 22 14"
    width="22"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      clipRule="evenodd"
      d="M19.5 1.25H2.5C1.80964 1.25 1.25 1.80964 1.25 2.5V11.5C1.25 12.1904 1.80964 12.75 2.5 12.75H19.5C20.1904 12.75 20.75 12.1904 20.75 11.5V2.5C20.75 1.80964 20.1904 1.25 19.5 1.25ZM2.5 0C1.11929 0 0 1.11929 0 2.5V11.5C0 12.8807 1.11929 14 2.5 14H19.5C20.8807 14 22 12.8807 22 11.5V2.5C22 1.11929 20.8807 0 19.5 0H2.5ZM3 3.5H4H4.25H4.6899L4.98715 3.82428L7 6.02011L9.01285 3.82428L9.3101 3.5H9.75H10H11V4.5V10.5H9V6.79807L7.73715 8.17572L7 8.97989L6.26285 8.17572L5 6.79807V10.5H3V4.5V3.5ZM15 7V3.5H17V7H19.5L17 9.5L16 10.5L15 9.5L12.5 7H15Z"
      fill="var(--ds-gray-700)"
      fillRule="evenodd"
    />
  </svg>
);

const LoveItIcon = ({ pathClassName }: { pathClassName: string }) => (
  <svg
    height="16"
    strokeLinejoin="round"
    viewBox="0 0 16 16"
    width="16"
  >
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M14.5 8C14.5 11.5899 11.5899 14.5 8 14.5C4.41015 14.5 1.5 11.5899 1.5 8C1.5 4.41015 4.41015 1.5 8 1.5C11.5899 1.5 14.5 4.41015 14.5 8ZM16 8C16 12.4183 12.4183 16 8 16C3.58172 16 0 12.4183 0 8C0 3.58172 3.58172 0 8 0C12.4183 0 16 3.58172 16 8ZM4.5 8.97498H3.875V9.59998C3.875 11.4747 5.81046 12.8637 7.99817 12.8637C10.1879 12.8637 12.125 11.4832 12.125 9.59998V8.97498H11.5H4.5ZM7.99817 11.6137C6.59406 11.6137 5.63842 10.9482 5.28118 10.225H10.7202C10.3641 10.9504 9.40797 11.6137 7.99817 11.6137Z"
    />
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M6.15295 4.92093L5.375 3.5L4.59705 4.92093L3 5.21885L4.11625 6.39495L3.90717 8L5.375 7.30593L6.84283 8L6.63375 6.39495L7.75 5.21885L6.15295 4.92093ZM11.403 4.92093L10.625 3.5L9.84705 4.92093L8.25 5.21885L9.36625 6.39495L9.15717 8L10.625 7.30593L12.0928 8L11.8837 6.39495L13 5.21885L11.403 4.92093Z"
      className={pathClassName}
    />
  </svg>
);

const ItsOkayIcon = () => (
  <svg
    height="16"
    strokeLinejoin="round"
    viewBox="0 0 16 16"
    width="16"
  >
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M14.5 8C14.5 11.5899 11.5899 14.5 8 14.5C4.41015 14.5 1.5 11.5899 1.5 8C1.5 4.41015 4.41015 1.5 8 1.5C11.5899 1.5 14.5 4.41015 14.5 8ZM16 8C16 12.4183 12.4183 16 8 16C3.58172 16 0 12.4183 0 8C0 3.58172 3.58172 0 8 0C12.4183 0 16 3.58172 16 8ZM11.5249 10.8478L11.8727 10.3286L10.8342 9.6329L10.4863 10.1522C9.94904 10.9543 9.0363 11.4802 8.00098 11.4802C6.96759 11.4802 6.05634 10.9563 5.51863 10.1567L5.16986 9.63804L4.13259 10.3356L4.48137 10.8542C5.2414 11.9844 6.53398 12.7302 8.00098 12.7302C9.47073 12.7302 10.7654 11.9816 11.5249 10.8478ZM6.75 6.75C6.75 7.30228 6.30228 7.75 5.75 7.75C5.19772 7.75 4.75 7.30228 4.75 6.75C4.75 6.19772 5.19772 5.75 5.75 5.75C6.30228 5.75 6.75 6.19772 6.75 6.75ZM10.25 7.75C10.8023 7.75 11.25 7.30228 11.25 6.75C11.25 6.19772 10.8023 5.75 10.25 5.75C9.69771 5.75 9.25 6.19772 9.25 6.75C9.25 7.30228 9.69771 7.75 10.25 7.75Z"
    />
  </svg>
);

const NotGreaterIcon = () => (
  <svg
    height="16"
    strokeLinejoin="round"
    viewBox="0 0 16 16"
    width="16"
  >
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M14.5 8C14.5 11.5899 11.5899 14.5 8 14.5C4.41015 14.5 1.5 11.5899 1.5 8C1.5 4.41015 4.41015 1.5 8 1.5C11.5899 1.5 14.5 4.41015 14.5 8ZM16 8C16 12.4183 12.4183 16 8 16C3.58172 16 0 12.4183 0 8C0 3.58172 3.58172 0 8 0C12.4183 0 16 3.58172 16 8ZM5.75 7.75C6.30228 7.75 6.75 7.30228 6.75 6.75C6.75 6.19772 6.30228 5.75 5.75 5.75C5.19772 5.75 4.75 6.19772 4.75 6.75C4.75 7.30228 5.19772 7.75 5.75 7.75ZM11.25 6.75C11.25 7.30228 10.8023 7.75 10.25 7.75C9.69771 7.75 9.25 7.30228 9.25 6.75C9.25 6.19772 9.69771 5.75 10.25 5.75C10.8023 5.75 11.25 6.19772 11.25 6.75ZM11.5249 11.2622L11.8727 11.7814L10.8342 12.4771L10.4863 11.9578C9.94904 11.1557 9.0363 10.6298 8.00098 10.6298C6.96759 10.6298 6.05634 11.1537 5.51863 11.9533L5.16986 12.4719L4.13259 11.7744L4.48137 11.2558C5.2414 10.1256 6.53398 9.37982 8.00098 9.37982C9.47073 9.37982 10.7654 10.1284 11.5249 11.2622Z"
    />
  </svg>
);

const HateIcon = () => (
  <svg
    height="16"
    strokeLinejoin="round"
    viewBox="0 0 16 16"
    width="16"
  >
    <path
      fillRule="evenodd"
      clipRule="evenodd" d="M4 9V16H5.5V9H4ZM12 9V16H10.5V9H12Z"
      fill="var(--ds-blue-700)"
    />
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M1.5 8C1.5 4.41015 4.41015 1.5 8 1.5C11.5899 1.5 14.5 4.41015 14.5 8C14.5 9.57941 13.9367 11.0273 13 12.1536V14.2454C14.8289 12.7793 16 10.5264 16 8C16 3.58172 12.4183 0 8 0C3.58172 0 0 3.58172 0 8C0 10.5264 1.17107 12.7793 3 14.2454V12.1536C2.06332 11.0273 1.5 9.57941 1.5 8ZM8 14.5C8.51627 14.5 9.01848 14.4398 9.5 14.3261V15.8596C9.01412 15.9518 8.51269 16 8 16C7.48731 16 6.98588 15.9518 6.5 15.8596V14.3261C6.98152 14.4398 7.48373 14.5 8 14.5ZM3.78568 8.36533C4.15863 7.98474 4.67623 7.75 5.25 7.75C5.82377 7.75 6.34137 7.98474 6.71432 8.36533L7.78568 7.31548C7.14222 6.65884 6.24318 6.25 5.25 6.25C4.25682 6.25 3.35778 6.65884 2.71432 7.31548L3.78568 8.36533ZM10.75 7.75C10.1762 7.75 9.65863 7.98474 9.28568 8.36533L8.21432 7.31548C8.85778 6.65884 9.75682 6.25 10.75 6.25C11.7432 6.25 12.6422 6.65884 13.2857 7.31548L12.2143 8.36533C11.8414 7.98474 11.3238 7.75 10.75 7.75ZM6.25 12H9.75C9.75 11.0335 8.9665 10.25 8 10.25C7.0335 10.25 6.25 11.0335 6.25 12Z"
    />
  </svg>
);

const Default = ({ label }: { label: string }) => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [selectedEmoji, setSelectedEmoji] = useState<number | null>(null);
  const [position, setPosition] = useState<{ top?: number, bottom?: number }>();
  const inputRef = useRef<HTMLButtonElement | null>(null);
  const menuRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const getPosition = () => {
      if (isOpen && inputRef && inputRef.current && menuRef.current) {
        const buttonRect = inputRef.current.getBoundingClientRect();
        const menuHeight = menuRef.current.offsetHeight;
        const viewportHeight = window.innerHeight;
        let _position;

        if (buttonRect.bottom + menuHeight <= viewportHeight) {
          _position = { top: buttonRect.height + 8 };
        } else if (buttonRect.top - menuHeight >= 0) {
          _position = { bottom: buttonRect.height + 8 };
        } else {
          _position = { top: buttonRect.height + 8 };
        }

        setPosition(_position);
      }
    };

    getPosition();

    window.addEventListener("resize", getPosition);
    window.addEventListener("scroll", getPosition);

    return () => {
      window.removeEventListener("resize", getPosition);
      window.removeEventListener("scroll", getPosition);
    };
  }, [isOpen]);

  useClickOutside(menuRef, () => setIsOpen(false));

  return (
    <div className="relative">
      <Button
        type="secondary"
        size="small"
        ref={inputRef}
        onClick={() => setIsOpen(true)}
        className="font-medium"
      >
        {label}
      </Button>
      <Material
        type="menu"
        className={clsx(
          "absolute bg-background-100 w-[340px] duration-200 font-sans left-1/2 -translate-x-1/2",
          isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
        )}
        style={{ ...position }}
        ref={menuRef}
      >
        <form>
          <div className="flex flex-col gap-2 p-2">
            <Textarea placeholder="Your feedback..." className="h-[100px]" />
            <div className="flex items-center gap-1 text-sm text-gray-900 ml-auto">
              <MSupportedIcon /> supported.
            </div>
          </div>
          <div className="flex justify-between p-3 bg-accents-1 border-t border-accents-2">
            <span className="flex items-center justify-start cursor-pointer">
              <Button
                variant="unstyled"
                svgOnly
                shape="rounded"
                className={clsx(
                  "group hover:!bg-blue-300 hover:fill-blue-900 !w-8 !h-8 p-0 duration-200",
                  selectedEmoji === 0 ? "!bg-blue-300 fill-blue-900" : "bg-transparent fill-gray-900"
                )}
                onClick={(event) => {
                  event.preventDefault();
                  setSelectedEmoji(selectedEmoji === 0 ? null : 0);
                }}
              >
                <LoveItIcon pathClassName={clsx(
                  "group-hover:fill-blue-900 duration-200",
                  selectedEmoji === 0 ? "fill-blue-900" : "fill-amber-800"
                )} />
              </Button>
              <Button
                variant="unstyled"
                svgOnly
                shape="rounded"
                className={clsx(
                  "hover:!bg-blue-300 hover:fill-blue-900 !w-8 !h-8 p-0 duration-200",
                  selectedEmoji === 1 ? "!bg-blue-300 fill-blue-900" : "bg-transparent fill-gray-900"
                )}
                onClick={(event) => {
                  event.preventDefault();
                  setSelectedEmoji(selectedEmoji === 1 ? null : 1);
                }}
              >
                <ItsOkayIcon />
              </Button>
              <Button
                variant="unstyled"
                svgOnly
                shape="rounded"
                className={clsx(
                  "hover:!bg-blue-300 hover:fill-blue-900 !w-8 !h-8 p-0 duration-200",
                  selectedEmoji === 2 ? "!bg-blue-300 fill-blue-900" : "bg-transparent fill-gray-900"
                )}
                onClick={(event) => {
                  event.preventDefault();
                  setSelectedEmoji(selectedEmoji === 2 ? null : 2);
                }}
              >
                <NotGreaterIcon />
              </Button>
              <Button
                variant="unstyled"
                svgOnly
                shape="rounded"
                className={clsx(
                  "hover:!bg-blue-300 hover:fill-blue-900 !w-8 !h-8 p-0 duration-200",
                  selectedEmoji === 3 ? "!bg-blue-300 fill-blue-900" : "bg-transparent fill-gray-900"
                )}
                onClick={(event) => {
                  event.preventDefault();
                  setSelectedEmoji(selectedEmoji === 3 ? null : 3);
                }}
              >
                <HateIcon />
              </Button>
            </span>
            <Button size="small">Send</Button>
          </div>
        </form>
      </Material>
    </div>
  );
};

const Inline = ({ label }: { label: string }) => {
  const [expanded, setExpanded] = useState<boolean>(false);
  const [selectedEmoji, setSelectedEmoji] = useState<number | null>(null);
  const textAreaRef = useRef<HTMLTextAreaElement | null>(null);
  const ref = useRef<HTMLDivElement | null>(null);
  const [showContent, setShowContent] = useState(false);

  useEffect(() => {
    if (expanded) {
      setShowContent(true);
      textAreaRef.current?.focus();
    } else {
      const timeout = setTimeout(() => setShowContent(false), 300);
      return () => clearTimeout(timeout);
    }
  }, [expanded]);

  useClickOutside(ref, () => {
    setExpanded(false);
    setSelectedEmoji(null);
  });

  return (
    <div
      className={clsx(
        "bg-background-100 shadow-border-small duration-200 overflow-hidden w-fit flex flex-col justify-start",
        expanded ? "max-h-[243px] rounded-xl" : "max-h-12 rounded-[30px]"
      )}
      ref={ref}
    >
      <div className={clsx("flex items-center justify-center gap-2 py-2 pl-4 pr-2 duration-200", expanded && "!px-[60px]")}>
        <p className="text-gray-900 text-sm">{label}</p>
        <div className="flex justify-between">
          <span className="flex items-center gap-[1px] cursor-pointer">
            <Button
              variant="unstyled"
              svgOnly
              shape="rounded"
              className={clsx(
                "group hover:!bg-blue-300 hover:fill-blue-900 !w-8 !h-8 p-0 duration-200",
                selectedEmoji === 0 ? "!bg-blue-300 fill-blue-900" : "bg-transparent fill-gray-900"
              )}
              onClick={(event) => {
                event.preventDefault();
                setSelectedEmoji(selectedEmoji === 0 ? null : 0);
                setExpanded(selectedEmoji !== 0);
              }}
            >
              <LoveItIcon pathClassName={clsx(
                "group-hover:fill-blue-900 duration-200",
                selectedEmoji === 0 ? "fill-blue-900" : "fill-amber-800"
              )} />
            </Button>
            <Button
              variant="unstyled"
              svgOnly
              shape="rounded"
              className={clsx(
                "hover:!bg-blue-300 hover:fill-blue-900 !w-8 !h-8 p-0 duration-200",
                selectedEmoji === 1 ? "!bg-blue-300 fill-blue-900" : "bg-transparent fill-gray-900"
              )}
              onClick={(event) => {
                event.preventDefault();
                setSelectedEmoji(selectedEmoji === 1 ? null : 1);
                setExpanded(selectedEmoji !== 1);
              }}
            >
              <ItsOkayIcon />
            </Button>
            <Button
              variant="unstyled"
              svgOnly
              shape="rounded"
              className={clsx(
                "hover:!bg-blue-300 hover:fill-blue-900 !w-8 !h-8 p-0 duration-200",
                selectedEmoji === 2 ? "!bg-blue-300 fill-blue-900" : "bg-transparent fill-gray-900"
              )}
              onClick={(event) => {
                event.preventDefault();
                setSelectedEmoji(selectedEmoji === 2 ? null : 2);
                setExpanded(selectedEmoji !== 2);
              }}
            >
              <NotGreaterIcon />
            </Button>
            <Button
              variant="unstyled"
              svgOnly
              shape="rounded"
              className={clsx(
                "hover:!bg-blue-300 hover:fill-blue-900 !w-8 !h-8 p-0 duration-200",
                selectedEmoji === 3 ? "!bg-blue-300 fill-blue-900" : "bg-transparent fill-gray-900"
              )}
              onClick={(event) => {
                event.preventDefault();
                setSelectedEmoji(selectedEmoji === 3 ? null : 3);
                setExpanded(selectedEmoji !== 3);
              }}
            >
              <HateIcon />
            </Button>
          </span>
        </div>
      </div>
      {showContent && (
        <form className="w-full transition-opacity duration-300 opacity-100">
          <div className="flex flex-col gap-2 p-2 w-full">
            <Textarea placeholder="Your feedback..." className="h-[100px]" ref={textAreaRef} />
            <div className="flex items-center gap-1 text-xs text-gray-900 ml-auto">
              <MSupportedIcon /> supported.
            </div>
          </div>
          <div className="flex justify-end p-3 bg-accents-1 border-t border-accents-2">
            <Button size="small">Send</Button>
          </div>
        </form>
      )}
    </div>
  );
};

export const Feedback = ({ type = "default", label }: FeedbackProps) => {
  return (type === "default" || type === undefined) ? <Default label={label} /> : <Inline label={label} />;
};

demo.tsx
import { Feedback } from "@/components/ui/feedback";

export default function InlineDemo() {
  return <Feedback type="inline" label="Was this helpful?" />;
}

```

Copy-paste these files for dependencies:
```tsx
shugar/material-1
import React from "react";
import clsx from "clsx";

const types = {
  base: "rounded-md shadow-border",
  small: "rounded-md shadow-border-small",
  medium: "rounded-xl shadow-border-medium",
  large: "rounded-xl shadow-border-large",
  tooltip: "rounded-md shadow-tooltip",
  menu: "rounded-xl shadow-menu",
  modal: "rounded-xl shadow-modal",
  fullscreen: "rounded-2xl shadow-fullscreen"
};

interface MaterialProps {
  type: keyof typeof types;
  children: React.ReactNode;
  className?: string;
  ref?: React.Ref<HTMLDivElement>;
  style?: React.CSSProperties;
  onClick?: (event: React.MouseEvent<HTMLDivElement>) => void;
}

export const Material = ({ type, children, className, ref, style, onClick }: MaterialProps) => {
  return (
    <div
      className={clsx(
        "bg-background-100",
        types[type],
        className
      )}
      ref={ref}
      style={style}
      onClick={onClick}
    >
      {children}
    </div>
  );
};
```
```tsx
shugar/button-1
import React from "react";
import { Spinner } from "@/components/ui/spinner-1";
import clsx from "clsx";

const sizes = [
  {
    tiny: "px-1.5 h-6 text-sm",
    small: "px-1.5 h-8 text-sm",
    medium: "px-2.5 h-10 text-sm",
    large: "px-3.5 h-12 text-base"
  },
  {
    tiny: "w-6 h-6 text-sm",
    small: "w-8 h-8 text-sm",
    medium: "w-10 h-10 text-sm",
    large: "w-12 h-12 text-base"
  }
];

const types = {
  primary: "bg-gray-1000 hover:bg-gray-1000-h text-background-100 fill-background-100",
  secondary: "bg-background-100 hover:bg-gray-alpha-200 text-gray-1000 fill-gray-1000 border border-gray-alpha-400",
  tertiary: "bg-none hover:bg-gray-alpha-200 text-gray-1000 fill-gray-1000",
  error: "bg-red-800 hover:bg-red-900 text-white fill-white",
  warning: "bg-amber-800 hover:bg-amber-850 text-black fill-black"
};

const shapes = {
  square: {
    tiny: "rounded",
    small: "rounded-md",
    medium: "rounded-md",
    large: "rounded-lg"
  },
  circle: {
    tiny: "rounded-[100%]",
    small: "rounded-[100%]",
    medium: "rounded-[100%]",
    large: "rounded-[100%]"
  },
  rounded: {
    tiny: "rounded-[100px]",
    small: "rounded-[100px]",
    medium: "rounded-[100px]",
    large: "rounded-[100px]"
  }
};

export interface ButtonProps {
  size?: keyof typeof sizes[0];
  type?: keyof typeof types;
  variant?: "styled" | "unstyled";
  shape?: keyof typeof shapes;
  svgOnly?: boolean;
  children?: React.ReactNode;
  prefix?: React.ReactNode;
  suffix?: React.ReactNode;
  shadow?: boolean;
  loading?: boolean;
  disabled?: boolean;
  fullWidth?: boolean;
  onClick?: React.MouseEventHandler<HTMLButtonElement>;
  ref?: React.Ref<HTMLButtonElement>;
  className?: string;
}

export const Button = ({
  size = "medium",
  type = "primary",
  variant = "styled",
  shape = "square",
  svgOnly = false,
  children,
  prefix,
  suffix,
  shadow = false,
  loading = false,
  disabled = false,
  fullWidth = false,
  onClick,
  ref,
  className,
  ...rest
}: ButtonProps) => {
  return (
    <button
      ref={ref}
      type="submit"
      disabled={disabled}
      onClick={onClick}
      tabIndex={0}
      className={clsx(
        "flex justify-center items-center gap-0.5 duration-150",
        sizes[+svgOnly][size],
        (disabled || loading) ? "bg-gray-100 text-gray-700 border border-gray-400 cursor-not-allowed" : types[type],
        shapes[shape][size],
        shadow && "shadow-border-small border-none",
        fullWidth && "w-full",
        variant === "unstyled" ? "outline-none px-0 h-fit bg-transparent hover:bg-transparent text-gray-1000" : "focus:shadow-focus-ring focus:outline-0",
        className
      )}
      {...rest}
    >
      {loading
        ? <Spinner size={size === "large" ? 24 : 16} />
        : prefix
      }
      <span className={clsx(
        "relative overflow-hidden whitespace-nowrap overflow-ellipsis font-sans",
        size !== "tiny" && variant !== "unstyled" && "px-1.5"
      )}>
        {children}
      </span>
      {!loading && suffix}
    </button>
  );
};
```
```tsx
shugar/spinner-1
import React from "react";

interface SpinnerProps {
  size?: number;
  color?: string;
}

const bars = [
  {
    animationDelay: "-1.2s",
    transform: "rotate(.0001deg) translate(146%)"
  },
  {
    animationDelay: "-1.1s",
    transform: "rotate(30deg) translate(146%)"
  },
  {
    animationDelay: "-1.0s",
    transform: "rotate(60deg) translate(146%)"
  },
  {
    animationDelay: "-0.9s",
    transform: "rotate(90deg) translate(146%)"
  },
  {
    animationDelay: "-0.8s",
    transform: "rotate(120deg) translate(146%)"
  },
  {
    animationDelay: "-0.7s",
    transform: "rotate(150deg) translate(146%)"
  },
  {
    animationDelay: "-0.6s",
    transform: "rotate(180deg) translate(146%)"
  },
  {
    animationDelay: "-0.5s",
    transform: "rotate(210deg) translate(146%)"
  },
  {
    animationDelay: "-0.4s",
    transform: "rotate(240deg) translate(146%)"
  },
  {
    animationDelay: "-0.3s",
    transform: "rotate(270deg) translate(146%)"
  },
  {
    animationDelay: "-0.2s",
    transform: "rotate(300deg) translate(146%)"
  },
  {
    animationDelay: "-0.1s",
    transform: "rotate(330deg) translate(146%)"
  }
];

export const Spinner = ({ size = 20, color = "#8f8f8f" }: SpinnerProps) => {
  return (
    <div style={{ width: size, height: size }}>
      <div className="relative top-1/2 left-1/2" style={{ width: size, height: size }}>
        {bars.map((item) => (
          <div
            key={item.transform}
            className="absolute h-[8%] w-[24%] -left-[10%] -top-[3.9%] rounded-[5px] animate-fade-spin"
            style={{ backgroundColor: color, ...item }}
          />
        ))}
      </div>
    </div>
  );
};
```
```tsx
shugar/textarea
import React, { useState } from "react";
import { Error } from "@/components/ui/error";
import clsx from "clsx";

interface TextareaProps {
  defaultValue?: string;
  placeholder?: string;
  disabled?: boolean;
  error?: string;
  size?: "xSmall" | "small" | "mediumSmall" | "large";
  style?: React.CSSProperties;
  value?: string;
  onChange?: (value?: string) => void;
  className?: string;
  ref?: React.Ref<HTMLTextAreaElement>;
}

export const Textarea = ({
  defaultValue,
  placeholder,
  disabled,
  error,
  size,
  style,
  value,
  onChange,
  className,
  ref
}: TextareaProps) => {
  const [_value, set_value] = useState(value);

  const _onChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    set_value(e.target.value);
    if (onChange) {
      onChange(e.target.value);
    }
  };

  return (
    <div className="w-full flex flex-col gap-2">
      <textarea
        className={clsx(
          "rounded-md resize-none font-sans bg-background-100 text-geist-foreground placeholder:text-gray-900 outline-none w-full duration-150 border border-gray-alpha-400 hover:border-gray-alpha-500 hover:ring-0",
          size === "large" ? "h-12 py-2.5 px-3 text-base" : "h-10 p-2.5 text-sm",
          disabled && "bg-gray-100 text-gray-700 placeholder:text-gray-700 placeholder:opacity-50 cursor-not-allowed",
          error ? "ring-red-300 ring-4 border-red-900 text-error" : "focus:border-gray-alpha-600 focus:shadow-focus-input",
          className
        )}
        defaultValue={defaultValue}
        placeholder={placeholder}
        disabled={disabled}
        style={style}
        autoComplete="off"
        autoCorrect="off"
        autoCapitalize="off"
        spellCheck="false"
        value={_value}
        onChange={_onChange}
        ref={ref}
      />
      {error && <Error size={size === "large" ? "large" : "small"}>{error}</Error>}
    </div>
  );
};
```
```tsx
shugar/error
import React from "react";

const ErrorIcon = () => (
  <svg
    height="16"
    strokeLinejoin="round"
    viewBox="0 0 16 16"
    width="16"
  >
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M5.30761 1.5L1.5 5.30761L1.5 10.6924L5.30761 14.5H10.6924L14.5 10.6924V5.30761L10.6924 1.5H5.30761ZM5.10051 0C4.83529 0 4.58094 0.105357 4.3934 0.292893L0.292893 4.3934C0.105357 4.58094 0 4.83529 0 5.10051V10.8995C0 11.1647 0.105357 11.4191 0.292894 11.6066L4.3934 15.7071C4.58094 15.8946 4.83529 16 5.10051 16H10.8995C11.1647 16 11.4191 15.8946 11.6066 15.7071L15.7071 11.6066C15.8946 11.4191 16 11.1647 16 10.8995V5.10051C16 4.83529 15.8946 4.58093 15.7071 4.3934L11.6066 0.292893C11.4191 0.105357 11.1647 0 10.8995 0H5.10051ZM8.75 3.75V4.5V8L8.75 8.75H7.25V8V4.5V3.75H8.75ZM8 12C8.55229 12 9 11.5523 9 11C9 10.4477 8.55229 10 8 10C7.44772 10 7 10.4477 7 11C7 11.5523 7.44772 12 8 12Z"
    />
  </svg>
);

const ErrorLinkIcon = () => (
  <svg
    height="16"
    strokeLinejoin="round"
    viewBox="0 0 16 16"
    width="16"
  >
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M11.5 9.75V11.25C11.5 11.3881 11.3881 11.5 11.25 11.5H4.75C4.61193 11.5 4.5 11.3881 4.5 11.25L4.5 4.75C4.5 4.61193 4.61193 4.5 4.75 4.5H6.25H7V3H6.25H4.75C3.7835 3 3 3.7835 3 4.75V11.25C3 12.2165 3.7835 13 4.75 13H11.25C12.2165 13 13 12.2165 13 11.25V9.75V9H11.5V9.75ZM8.5 3H9.25H12.2495C12.6637 3 12.9995 3.33579 12.9995 3.75V6.75V7.5H11.4995V6.75V5.56066L8.53033 8.52978L8 9.06011L6.93934 7.99945L7.46967 7.46912L10.4388 4.5H9.25H8.5V3Z"
    />
  </svg>
);

interface Error {
  message: string;
  action: string;
  link: string;
}

interface ErrorProps {
  error?: Error;
  label?: string;
  size?: "small" | "medium" | "large";
  children?: React.ReactNode;
}

export const Error = ({ error, label, size = "medium", children }: ErrorProps) => {
  return (
    <div
      className={
        `flex items-center gap-2 text-red-900 fill-red-900 font-sans
      ${{
          small: "text-[13px] leading-5",
          medium: "text-sm",
          large: "text-base"
        }[size]}`
      }
      // @ts-ignore
      style={{ "--geist-link-color": "var(--ds-red-900)" }}
    >
      <ErrorIcon />
      {error ? (
        <>
          {error.message}
          <a
            className="font-medium flex items-center gap-0.5 -ml-1 hover:no-underline hover:opacity-60 duration-150 relative after:content-[''] after:absolute after:left-0 after:bottom-0 after:w-full after:h-[1px] after:bg-red-900"
            href={error.link}
            target="_blank"
          >
            {error.action}
            <ErrorLinkIcon />
          </a>
        </>
      ) : (
        <>
          {label && <span className="font-medium">{label}:</span>}
          {children}
        </>
      )}
    </div>
  );
};
```
```tsx
shugar/use-click-outside
import { RefObject, useEffect } from "react";

export const useClickOutside = (ref: RefObject<any>, callback: () => void) => {
  useEffect(() => {
    function handleClickOutside(event: Event) {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        callback();
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("touchstart", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("touchstart", handleClickOutside);
    };
  }, [ref]);
};
```

Install NPM dependencies:
```bash
clsx
```

Extend existing Tailwind 4 index.css with this code (or if project uses Tailwind 3, extend tailwind.config.js or globals.css):
```css
@import "tailwindcss";
@import "tw-animate-css";

@theme inline {
  --color-context-card-border: var(--context-card-border);
  --color-red-800: var(--ds-red-800);
  --color-red-900: var(--ds-red-900);
  --color-blue-300: var(--ds-blue-300);
  --color-blue-900: var(--ds-blue-900);
  --color-amber-800: var(--ds-amber-800);
  --color-amber-850: var(--ds-amber-850);
  --color-gray-100: var(--ds-gray-100);
  --color-gray-400: var(--ds-gray-400);
  --color-gray-700: var(--ds-gray-700);
  --color-gray-1000: var(--ds-gray-1000);
  --color-gray-1000-h: var(--ds-gray-1000-h);
  --color-gray-alpha-200: var(--ds-gray-alpha-200);
  --color-gray-alpha-400: var(--ds-gray-alpha-400);
  --color-background-100: var(--ds-background-100);
  --color-red-300: var(--ds-red-300);
  --color-gray-900: var(--ds-gray-900);
  --color-gray-alpha-500: var(--ds-gray-alpha-500);
  --color-gray-alpha-600: var(--ds-gray-alpha-600);
  --color-geist-foreground: var(--geist-foreground);
  --color-error: var(--geist-error);
  --color-accents-1: var(--accents-1);
  --color-accents-2: var(--accents-2);
  --shadow-focus-ring: var(--ds-focus-ring);
  --shadow-border-small: var(--ds-shadow-border-small);
  --shadow-focus-input: var(--ds-input-ring);
  --shadow-border: var(--ds-shadow-border);
  --shadow-border-medium: var(--ds-shadow-border-medium);
  --shadow-border-large: var(--ds-shadow-border-large);
  --shadow-tooltip: var(--ds-shadow-tooltip);
  --shadow-menu: var(--ds-shadow-menu);
  --shadow-modal: var(--ds-shadow-modal);
  --shadow-fullscreen: var(--ds-shadow-fullscreen);
}

:root {
  --context-card-border: hsla(0, 0%, 92%, 1);
  --ds-blue-300: oklch(94.58% 0.0293 249.84870859673202);
  --ds-blue-900: oklch(53.18% 0.2399 256.9900584162342);
  --accents-1: #fafafa;
  --accents-2: #eaeaea;
  --ds-red-800: oklch(58.19% 0.2482 25.15);
  --ds-red-900: oklch(54.99% 0.232 25.29);
  --ds-blue-700: oklch(57.61% 0.2508 258.23);
  --ds-amber-800: oklch(77.21% 0.1991 64.28);
  --ds-amber-850: hsl(33, 96%, 42%);
  --ds-gray-100: hsla(0, 0%, 95%, 1);
  --ds-gray-400: hsla(0, 0%, 92%, 1);
  --ds-gray-700: hsla(0, 0%, 56%, 1);
  --ds-gray-1000: hsla(0, 0%, 9%, 1);
  --ds-gray-1000-h: hsl(0, 0%, 22%);
  --ds-gray-alpha-200: hsla(0, 0%, 0%, 0.08);
  --ds-gray-alpha-400: hsla(0, 0%, 0%, 0.08);
  --ds-background-100: hsla(0, 0%, 100%, 1);
  --ds-focus-color: var(--ds-blue-700);
  --ds-focus-ring: 0 0 0 2px var(--ds-background-100), 0 0 0 4px var(--ds-focus-color);
  --ds-shadow-border: 0 0 0 1px rgba(0, 0, 0, 0.08);
  --ds-shadow-small: 0px 2px 2px rgba(0, 0, 0, 0.04);
  --ds-red-300: oklch(94.33% 0.0369 15.011509923860523);
  --ds-gray-900: hsla(0, 0%, 40%, 1);
  --ds-gray-alpha-500: hsla(0, 0%, 0%, 0.21);
  --ds-gray-alpha-600: hsla(0, 0%, 0%, 0.34);
  --geist-foreground: #000;
  --geist-error: #ee0000;
  --ds-input-ring: 0 0 0 1px var(--ds-gray-alpha-600), 0 0 0 4px rgba(0, 0, 0, .16);
  --ds-shadow-border-small: var(--ds-shadow-border), var(--ds-shadow-small);
  --ds-shadow-medium: 0px 2px 2px rgba(0, 0, 0, 0.04), 0px 8px 8px -8px rgba(0, 0, 0, 0.04);
  --ds-shadow-border-medium: var(--ds-shadow-border), var(--ds-shadow-medium);
  --ds-shadow-large: 0px 2px 2px rgba(0, 0, 0, 0.04), 0px 8px 16px -4px rgba(0, 0, 0, 0.04);
  --ds-shadow-border-large: var(--ds-shadow-border), var(--ds-shadow-large);
  --ds-shadow-tooltip: var(--ds-shadow-border), 0px 1px 1px rgba(0, 0, 0, 0.02), 0px 4px 8px rgba(0, 0, 0, 0.04);
  --ds-shadow-menu: var(--ds-shadow-border), 0px 1px 1px rgba(0, 0, 0, 0.02), 0px 4px 8px -4px rgba(0, 0, 0, 0.04), 0px 16px 24px -8px rgba(0, 0, 0, 0.06);
  --ds-shadow-modal: var(--ds-shadow-border), 0px 1px 1px rgba(0, 0, 0, 0.02), 0px 8px 16px -4px rgba(0, 0, 0, 0.04), 0px 24px 32px -8px rgba(0, 0, 0, 0.06);
  --ds-shadow-fullscreen: var(--ds-shadow-border), 0px 1px 1px rgba(0, 0, 0, 0.02), 0px 8px 16px -4px rgba(0, 0, 0, 0.04), 0px 24px 32px -8px rgba(0, 0, 0, 0.06);
}

.dark {
  --context-card-border: hsla(0, 0%, 18%, 1);
  --ds-blue-300: oklch(30.86% 0.1022 255.21);
  --ds-blue-900: oklch(71.7% 0.1648 250.79360374054167);
  --accents-2: #333333;
  --accents-1: #111111;
  --ds-red-800: oklch(58.01% 0.227 25.12);
  --ds-red-900: oklch(69.96% 0.2136 22.03);
  --ds-blue-700: oklch(57.61% 0.2321 258.23);
  --ds-amber-800: oklch(77.21% 0.1991 64.28);
  --ds-gray-100: hsla(0, 0%, 10%, 1);
  --ds-gray-400: hsla(0, 0%, 18%, 1);
  --ds-gray-700: hsla(0, 0%, 56%, 1);
  --ds-gray-1000: hsla(0, 0%, 93%, 1);
  --ds-gray-1000-h: hsl(0, 0%, 80%);
  --ds-gray-alpha-200: hsla(0, 0%, 100%, 0.09);
  --ds-gray-alpha-400: hsla(0, 0%, 100%, 0.14);
  --ds-background-100: hsla(0,0%,4%, 1);
  --ds-shadow-border: 0 0 0 1px rgba(255, 255, 255, 0.145);
  --ds-shadow-small: 0px 1px 2px rgba(0, 0, 0, 0.16);
  --ds-red-300: oklch(31.47% 0.1105 20.96);
  --ds-gray-900: hsla(0, 0%, 63%, 1);
  --ds-gray-alpha-500: hsla(0, 0%, 100%, 0.24);
  --ds-gray-alpha-600: hsla(0, 0%, 100%, 0.51);
  --geist-foreground: #fff;
  --geist-error: #ff0000;
  --ds-input-ring: 0 0 0 1px var(--ds-gray-alpha-600), 0 0 0 4px rgba(255, 255, 255, .24);
  --ds-shadow-border-small: var(--ds-shadow-border), 0px 1px 2px rgba(0, 0, 0, 0.16);
  --ds-shadow-medium: 0px 2px 2px rgba(0, 0, 0, 0.32), 0px 8px 8px -8px rgba(0, 0, 0, 0.16);
  --ds-shadow-border-medium: var(--ds-shadow-border), 0px 2px 2px rgba(0, 0, 0, 0.32), 0px 8px 8px -8px rgba(0, 0, 0, 0.16);
  --ds-shadow-large: 0px 2px 2px rgba(0, 0, 0, 0.04), 0px 8px 16px -4px rgba(0, 0, 0, 0.04);
  --ds-shadow-border-large: var(--ds-shadow-border), 0px 2px 2px rgba(0, 0, 0, 0.04), 0px 8px 16px -4px rgba(0, 0, 0, 0.04);
  --ds-shadow-tooltip: var(--ds-shadow-border), 0px 1px 1px rgba(0, 0, 0, 0.02), 0px 4px 8px rgba(0, 0, 0, 0.04);
  --ds-shadow-menu: var(--ds-shadow-border), 0px 1px 1px rgba(0, 0, 0, 0.02), 0px 4px 8px -4px rgba(0, 0, 0, 0.04), 0px 16px 24px -8px rgba(0, 0, 0, 0.06);
  --ds-shadow-modal: var(--ds-shadow-border), 0px 1px 1px rgba(0, 0, 0, 0.02), 0px 8px 16px -4px rgba(0, 0, 0, 0.04), 0px 24px 32px -8px rgba(0, 0, 0, 0.06);
  --ds-shadow-fullscreen: var(--ds-shadow-border), 0px 1px 1px rgba(0, 0, 0, 0.02), 0px 8px 16px -4px rgba(0, 0, 0, 0.04), 0px 24px 32px -8px rgba(0, 0, 0, 0.06);
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
import React, { useEffect, useRef, useState } from "react";
import { Button } from "@/components/ui/button-1";
import { Material } from "@/components/ui/material-1";
import { Textarea } from "@/components/ui/textarea";
import clsx from "clsx";
import { useClickOutside } from "@/components/ui/use-click-outside";

interface FeedbackProps {
  label: string;
  type?: "default" | "inline";
}

const MSupportedIcon = () => (
  <svg
    fill="none"
    height="14"
    viewBox="0 0 22 14"
    width="22"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      clipRule="evenodd"
      d="M19.5 1.25H2.5C1.80964 1.25 1.25 1.80964 1.25 2.5V11.5C1.25 12.1904 1.80964 12.75 2.5 12.75H19.5C20.1904 12.75 20.75 12.1904 20.75 11.5V2.5C20.75 1.80964 20.1904 1.25 19.5 1.25ZM2.5 0C1.11929 0 0 1.11929 0 2.5V11.5C0 12.8807 1.11929 14 2.5 14H19.5C20.8807 14 22 12.8807 22 11.5V2.5C22 1.11929 20.8807 0 19.5 0H2.5ZM3 3.5H4H4.25H4.6899L4.98715 3.82428L7 6.02011L9.01285 3.82428L9.3101 3.5H9.75H10H11V4.5V10.5H9V6.79807L7.73715 8.17572L7 8.97989L6.26285 8.17572L5 6.79807V10.5H3V4.5V3.5ZM15 7V3.5H17V7H19.5L17 9.5L16 10.5L15 9.5L12.5 7H15Z"
      fill="var(--ds-gray-700)"
      fillRule="evenodd"
    />
  </svg>
);

const LoveItIcon = ({ pathClassName }: { pathClassName: string }) => (
  <svg
    height="16"
    strokeLinejoin="round"
    viewBox="0 0 16 16"
    width="16"
  >
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M14.5 8C14.5 11.5899 11.5899 14.5 8 14.5C4.41015 14.5 1.5 11.5899 1.5 8C1.5 4.41015 4.41015 1.5 8 1.5C11.5899 1.5 14.5 4.41015 14.5 8ZM16 8C16 12.4183 12.4183 16 8 16C3.58172 16 0 12.4183 0 8C0 3.58172 3.58172 0 8 0C12.4183 0 16 3.58172 16 8ZM4.5 8.97498H3.875V9.59998C3.875 11.4747 5.81046 12.8637 7.99817 12.8637C10.1879 12.8637 12.125 11.4832 12.125 9.59998V8.97498H11.5H4.5ZM7.99817 11.6137C6.59406 11.6137 5.63842 10.9482 5.28118 10.225H10.7202C10.3641 10.9504 9.40797 11.6137 7.99817 11.6137Z"
    />
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M6.15295 4.92093L5.375 3.5L4.59705 4.92093L3 5.21885L4.11625 6.39495L3.90717 8L5.375 7.30593L6.84283 8L6.63375 6.39495L7.75 5.21885L6.15295 4.92093ZM11.403 4.92093L10.625 3.5L9.84705 4.92093L8.25 5.21885L9.36625 6.39495L9.15717 8L10.625 7.30593L12.0928 8L11.8837 6.39495L13 5.21885L11.403 4.92093Z"
      className={pathClassName}
    />
  </svg>
);

const ItsOkayIcon = () => (
  <svg
    height="16"
    strokeLinejoin="round"
    viewBox="0 0 16 16"
    width="16"
  >
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M14.5 8C14.5 11.5899 11.5899 14.5 8 14.5C4.41015 14.5 1.5 11.5899 1.5 8C1.5 4.41015 4.41015 1.5 8 1.5C11.5899 1.5 14.5 4.41015 14.5 8ZM16 8C16 12.4183 12.4183 16 8 16C3.58172 16 0 12.4183 0 8C0 3.58172 3.58172 0 8 0C12.4183 0 16 3.58172 16 8ZM11.5249 10.8478L11.8727 10.3286L10.8342 9.6329L10.4863 10.1522C9.94904 10.9543 9.0363 11.4802 8.00098 11.4802C6.96759 11.4802 6.05634 10.9563 5.51863 10.1567L5.16986 9.63804L4.13259 10.3356L4.48137 10.8542C5.2414 11.9844 6.53398 12.7302 8.00098 12.7302C9.47073 12.7302 10.7654 11.9816 11.5249 10.8478ZM6.75 6.75C6.75 7.30228 6.30228 7.75 5.75 7.75C5.19772 7.75 4.75 7.30228 4.75 6.75C4.75 6.19772 5.19772 5.75 5.75 5.75C6.30228 5.75 6.75 6.19772 6.75 6.75ZM10.25 7.75C10.8023 7.75 11.25 7.30228 11.25 6.75C11.25 6.19772 10.8023 5.75 10.25 5.75C9.69771 5.75 9.25 6.19772 9.25 6.75C9.25 7.30228 9.69771 7.75 10.25 7.75Z"
    />
  </svg>
);

const NotGreaterIcon = () => (
  <svg
    height="16"
    strokeLinejoin="round"
    viewBox="0 0 16 16"
    width="16"
  >
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M14.5 8C14.5 11.5899 11.5899 14.5 8 14.5C4.41015 14.5 1.5 11.5899 1.5 8C1.5 4.41015 4.41015 1.5 8 1.5C11.5899 1.5 14.5 4.41015 14.5 8ZM16 8C16 12.4183 12.4183 16 8 16C3.58172 16 0 12.4183 0 8C0 3.58172 3.58172 0 8 0C12.4183 0 16 3.58172 16 8ZM5.75 7.75C6.30228 7.75 6.75 7.30228 6.75 6.75C6.75 6.19772 6.30228 5.75 5.75 5.75C5.19772 5.75 4.75 6.19772 4.75 6.75C4.75 7.30228 5.19772 7.75 5.75 7.75ZM11.25 6.75C11.25 7.30228 10.8023 7.75 10.25 7.75C9.69771 7.75 9.25 7.30228 9.25 6.75C9.25 6.19772 9.69771 5.75 10.25 5.75C10.8023 5.75 11.25 6.19772 11.25 6.75ZM11.5249 11.2622L11.8727 11.7814L10.8342 12.4771L10.4863 11.9578C9.94904 11.1557 9.0363 10.6298 8.00098 10.6298C6.96759 10.6298 6.05634 11.1537 5.51863 11.9533L5.16986 12.4719L4.13259 11.7744L4.48137 11.2558C5.2414 10.1256 6.53398 9.37982 8.00098 9.37982C9.47073 9.37982 10.7654 10.1284 11.5249 11.2622Z"
    />
  </svg>
);

const HateIcon = () => (
  <svg
    height="16"
    strokeLinejoin="round"
    viewBox="0 0 16 16"
    width="16"
  >
    <path
      fillRule="evenodd"
      clipRule="evenodd" d="M4 9V16H5.5V9H4ZM12 9V16H10.5V9H12Z"
      fill="var(--ds-blue-700)"
    />
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M1.5 8C1.5 4.41015 4.41015 1.5 8 1.5C11.5899 1.5 14.5 4.41015 14.5 8C14.5 9.57941 13.9367 11.0273 13 12.1536V14.2454C14.8289 12.7793 16 10.5264 16 8C16 3.58172 12.4183 0 8 0C3.58172 0 0 3.58172 0 8C0 10.5264 1.17107 12.7793 3 14.2454V12.1536C2.06332 11.0273 1.5 9.57941 1.5 8ZM8 14.5C8.51627 14.5 9.01848 14.4398 9.5 14.3261V15.8596C9.01412 15.9518 8.51269 16 8 16C7.48731 16 6.98588 15.9518 6.5 15.8596V14.3261C6.98152 14.4398 7.48373 14.5 8 14.5ZM3.78568 8.36533C4.15863 7.98474 4.67623 7.75 5.25 7.75C5.82377 7.75 6.34137 7.98474 6.71432 8.36533L7.78568 7.31548C7.14222 6.65884 6.24318 6.25 5.25 6.25C4.25682 6.25 3.35778 6.65884 2.71432 7.31548L3.78568 8.36533ZM10.75 7.75C10.1762 7.75 9.65863 7.98474 9.28568 8.36533L8.21432 7.31548C8.85778 6.65884 9.75682 6.25 10.75 6.25C11.7432 6.25 12.6422 6.65884 13.2857 7.31548L12.2143 8.36533C11.8414 7.98474 11.3238 7.75 10.75 7.75ZM6.25 12H9.75C9.75 11.0335 8.9665 10.25 8 10.25C7.0335 10.25 6.25 11.0335 6.25 12Z"
    />
  </svg>
);

const Default = ({ label }: { label: string }) => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [selectedEmoji, setSelectedEmoji] = useState<number | null>(null);
  const [position, setPosition] = useState<{ top?: number, bottom?: number }>();
  const inputRef = useRef<HTMLButtonElement | null>(null);
  const menuRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const getPosition = () => {
      if (isOpen && inputRef && inputRef.current && menuRef.current) {
        const buttonRect = inputRef.current.getBoundingClientRect();
        const menuHeight = menuRef.current.offsetHeight;
        const viewportHeight = window.innerHeight;
        let _position;

        if (buttonRect.bottom + menuHeight <= viewportHeight) {
          _position = { top: buttonRect.height + 8 };
        } else if (buttonRect.top - menuHeight >= 0) {
          _position = { bottom: buttonRect.height + 8 };
        } else {
          _position = { top: buttonRect.height + 8 };
        }

        setPosition(_position);
      }
    };

    getPosition();

    window.addEventListener("resize", getPosition);
    window.addEventListener("scroll", getPosition);

    return () => {
      window.removeEventListener("resize", getPosition);
      window.removeEventListener("scroll", getPosition);
    };
  }, [isOpen]);

  useClickOutside(menuRef, () => setIsOpen(false));

  return (
    <div className="relative">
      <Button
        type="secondary"
        size="small"
        ref={inputRef}
        onClick={() => setIsOpen(true)}
        className="font-medium"
      >
        {label}
      </Button>
      <Material
        type="menu"
        className={clsx(
          "absolute bg-background-100 w-[340px] duration-200 font-sans left-1/2 -translate-x-1/2",
          isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
        )}
        style={{ ...position }}
        ref={menuRef}
      >
        <form>
          <div className="flex flex-col gap-2 p-2">
            <Textarea placeholder="Your feedback..." className="h-[100px]" />
            <div className="flex items-center gap-1 text-sm text-gray-900 ml-auto">
              <MSupportedIcon /> supported.
            </div>
          </div>
          <div className="flex justify-between p-3 bg-accents-1 border-t border-accents-2">
            <span className="flex items-center justify-start cursor-pointer">
              <Button
                variant="unstyled"
                svgOnly
                shape="rounded"
                className={clsx(
                  "group hover:!bg-blue-300 hover:fill-blue-900 !w-8 !h-8 p-0 duration-200",
                  selectedEmoji === 0 ? "!bg-blue-300 fill-blue-900" : "bg-transparent fill-gray-900"
                )}
                onClick={(event) => {
                  event.preventDefault();
                  setSelectedEmoji(selectedEmoji === 0 ? null : 0);
                }}
              >
                <LoveItIcon pathClassName={clsx(
                  "group-hover:fill-blue-900 duration-200",
                  selectedEmoji === 0 ? "fill-blue-900" : "fill-amber-800"
                )} />
              </Button>
              <Button
                variant="unstyled"
                svgOnly
                shape="rounded"
                className={clsx(
                  "hover:!bg-blue-300 hover:fill-blue-900 !w-8 !h-8 p-0 duration-200",
                  selectedEmoji === 1 ? "!bg-blue-300 fill-blue-900" : "bg-transparent fill-gray-900"
                )}
                onClick={(event) => {
                  event.preventDefault();
                  setSelectedEmoji(selectedEmoji === 1 ? null : 1);
                }}
              >
                <ItsOkayIcon />
              </Button>
              <Button
                variant="unstyled"
                svgOnly
                shape="rounded"
                className={clsx(
                  "hover:!bg-blue-300 hover:fill-blue-900 !w-8 !h-8 p-0 duration-200",
                  selectedEmoji === 2 ? "!bg-blue-300 fill-blue-900" : "bg-transparent fill-gray-900"
                )}
                onClick={(event) => {
                  event.preventDefault();
                  setSelectedEmoji(selectedEmoji === 2 ? null : 2);
                }}
              >
                <NotGreaterIcon />
              </Button>
              <Button
                variant="unstyled"
                svgOnly
                shape="rounded"
                className={clsx(
                  "hover:!bg-blue-300 hover:fill-blue-900 !w-8 !h-8 p-0 duration-200",
                  selectedEmoji === 3 ? "!bg-blue-300 fill-blue-900" : "bg-transparent fill-gray-900"
                )}
                onClick={(event) => {
                  event.preventDefault();
                  setSelectedEmoji(selectedEmoji === 3 ? null : 3);
                }}
              >
                <HateIcon />
              </Button>
            </span>
            <Button size="small">Send</Button>
          </div>
        </form>
      </Material>
    </div>
  );
};

const Inline = ({ label }: { label: string }) => {
  const [expanded, setExpanded] = useState<boolean>(false);
  const [selectedEmoji, setSelectedEmoji] = useState<number | null>(null);
  const textAreaRef = useRef<HTMLTextAreaElement | null>(null);
  const ref = useRef<HTMLDivElement | null>(null);
  const [showContent, setShowContent] = useState(false);

  useEffect(() => {
    if (expanded) {
      setShowContent(true);
      textAreaRef.current?.focus();
    } else {
      const timeout = setTimeout(() => setShowContent(false), 300);
      return () => clearTimeout(timeout);
    }
  }, [expanded]);

  useClickOutside(ref, () => {
    setExpanded(false);
    setSelectedEmoji(null);
  });

  return (
    <div
      className={clsx(
        "bg-background-100 shadow-border-small duration-200 overflow-hidden w-fit flex flex-col justify-start",
        expanded ? "max-h-[243px] rounded-xl" : "max-h-12 rounded-[30px]"
      )}
      ref={ref}
    >
      <div className={clsx("flex items-center justify-center gap-2 py-2 pl-4 pr-2 duration-200", expanded && "!px-[60px]")}>
        <p className="text-gray-900 text-sm">{label}</p>
        <div className="flex justify-between">
          <span className="flex items-center gap-[1px] cursor-pointer">
            <Button
              variant="unstyled"
              svgOnly
              shape="rounded"
              className={clsx(
                "group hover:!bg-blue-300 hover:fill-blue-900 !w-8 !h-8 p-0 duration-200",
                selectedEmoji === 0 ? "!bg-blue-300 fill-blue-900" : "bg-transparent fill-gray-900"
              )}
              onClick={(event) => {
                event.preventDefault();
                setSelectedEmoji(selectedEmoji === 0 ? null : 0);
                setExpanded(selectedEmoji !== 0);
              }}
            >
              <LoveItIcon pathClassName={clsx(
                "group-hover:fill-blue-900 duration-200",
                selectedEmoji === 0 ? "fill-blue-900" : "fill-amber-800"
              )} />
            </Button>
            <Button
              variant="unstyled"
              svgOnly
              shape="rounded"
              className={clsx(
                "hover:!bg-blue-300 hover:fill-blue-900 !w-8 !h-8 p-0 duration-200",
                selectedEmoji === 1 ? "!bg-blue-300 fill-blue-900" : "bg-transparent fill-gray-900"
              )}
              onClick={(event) => {
                event.preventDefault();
                setSelectedEmoji(selectedEmoji === 1 ? null : 1);
                setExpanded(selectedEmoji !== 1);
              }}
            >
              <ItsOkayIcon />
            </Button>
            <Button
              variant="unstyled"
              svgOnly
              shape="rounded"
              className={clsx(
                "hover:!bg-blue-300 hover:fill-blue-900 !w-8 !h-8 p-0 duration-200",
                selectedEmoji === 2 ? "!bg-blue-300 fill-blue-900" : "bg-transparent fill-gray-900"
              )}
              onClick={(event) => {
                event.preventDefault();
                setSelectedEmoji(selectedEmoji === 2 ? null : 2);
                setExpanded(selectedEmoji !== 2);
              }}
            >
              <NotGreaterIcon />
            </Button>
            <Button
              variant="unstyled"
              svgOnly
              shape="rounded"
              className={clsx(
                "hover:!bg-blue-300 hover:fill-blue-900 !w-8 !h-8 p-0 duration-200",
                selectedEmoji === 3 ? "!bg-blue-300 fill-blue-900" : "bg-transparent fill-gray-900"
              )}
              onClick={(event) => {
                event.preventDefault();
                setSelectedEmoji(selectedEmoji === 3 ? null : 3);
                setExpanded(selectedEmoji !== 3);
              }}
            >
              <HateIcon />
            </Button>
          </span>
        </div>
      </div>
      {showContent && (
        <form className="w-full transition-opacity duration-300 opacity-100">
          <div className="flex flex-col gap-2 p-2 w-full">
            <Textarea placeholder="Your feedback..." className="h-[100px]" ref={textAreaRef} />
            <div className="flex items-center gap-1 text-xs text-gray-900 ml-auto">
              <MSupportedIcon /> supported.
            </div>
          </div>
          <div className="flex justify-end p-3 bg-accents-1 border-t border-accents-2">
            <Button size="small">Send</Button>
          </div>
        </form>
      )}
    </div>
  );
};

export const Feedback = ({ type = "default", label }: FeedbackProps) => {
  return (type === "default" || type === undefined) ? <Default label={label} /> : <Inline label={label} />;
};