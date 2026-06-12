https://21st.dev/community/components/chetanverma16/video-player/default
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
video-player.tsx
"use client";

import React, { useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Play, Pause, Volume2, Volume1, VolumeX } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";

const formatTime = (seconds: number) => {
const minutes = Math.floor(seconds / 60);
const remainingSeconds = Math.floor(seconds % 60);
return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`;
};

const CustomSlider = ({
value,
onChange,
className,
}: {
value: number;
onChange: (value: number) => void;
className?: string;
}) => {
return (
  <motion.div
    className={cn(
      "relative w-full h-1 bg-white/20 rounded-full cursor-pointer",
      className
    )}
    onClick={(e) => {
      const rect = e.currentTarget.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const percentage = (x / rect.width) * 100;
      onChange(Math.min(Math.max(percentage, 0), 100));
    }}
  >
    <motion.div
      className="absolute top-0 left-0 h-full bg-white rounded-full"
      style={{ width: `${value}%` }}
      initial={{ width: 0 }}
      animate={{ width: `${value}%` }}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
    />
  </motion.div>
);
};

const VideoPlayer = ({ src }: { src: string }) => {
const videoRef = useRef<HTMLVideoElement>(null);
const [isPlaying, setIsPlaying] = useState(false);
const [volume, setVolume] = useState(1);
const [progress, setProgress] = useState(0);
const [isMuted, setIsMuted] = useState(false);
const [playbackSpeed, setPlaybackSpeed] = useState(1);
const [showControls, setShowControls] = useState(false);
const [currentTime, setCurrentTime] = useState(0);
const [duration, setDuration] = useState(0);

const togglePlay = () => {
  if (videoRef.current) {
    if (isPlaying) {
      videoRef.current.pause();
    } else {
      videoRef.current.play();
    }
    setIsPlaying(!isPlaying);
  }
};

const handleVolumeChange = (value: number) => {
  if (videoRef.current) {
    const newVolume = value / 100;
    videoRef.current.volume = newVolume;
    setVolume(newVolume);
    setIsMuted(newVolume === 0);
  }
};

const handleTimeUpdate = () => {
  if (videoRef.current) {
    const progress =
      (videoRef.current.currentTime / videoRef.current.duration) * 100;
    setProgress(isFinite(progress) ? progress : 0);
    setCurrentTime(videoRef.current.currentTime);
    setDuration(videoRef.current.duration);
  }
};

const handleSeek = (value: number) => {
  if (videoRef.current && videoRef.current.duration) {
    const time = (value / 100) * videoRef.current.duration;
    if (isFinite(time)) {
      videoRef.current.currentTime = time;
      setProgress(value);
    }
  }
};

const toggleMute = () => {
  if (videoRef.current) {
    videoRef.current.muted = !isMuted;
    setIsMuted(!isMuted);
    if (!isMuted) {
      setVolume(0);
    } else {
      setVolume(1);
      videoRef.current.volume = 1;
    }
  }
};

const setSpeed = (speed: number) => {
  if (videoRef.current) {
    videoRef.current.playbackRate = speed;
    setPlaybackSpeed(speed);
  }
};

return (
  <motion.div
    className="relative w-full max-w-4xl mx-auto rounded-xl overflow-hidden bg-[#11111198] shadow-[0_0_20px_rgba(0,0,0,0.2)] backdrop-blur-sm"
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5 }}
    onMouseEnter={() => setShowControls(true)}
    onMouseLeave={() => setShowControls(false)}
  >
    <video
      ref={videoRef}
      className="w-full"
      onTimeUpdate={handleTimeUpdate}
      src={src}
      onClick={togglePlay}
    />

    <AnimatePresence>
      {showControls && (
        <motion.div
          className="absolute bottom-0 mx-auto max-w-xl left-0 right-0 p-4 m-2 bg-[#11111198] backdrop-blur-md rounded-2xl"
          initial={{ y: 20, opacity: 0, filter: "blur(10px)" }}
          animate={{ y: 0, opacity: 1, filter: "blur(0px)" }}
          exit={{ y: 20, opacity: 0, filter: "blur(10px)" }}
          transition={{ duration: 0.6, ease: "circInOut", type: "spring" }}
        >
          <div className="flex items-center gap-2 mb-2">
            <span className="text-white text-sm">
              {formatTime(currentTime)}
            </span>
            <CustomSlider
              value={progress}
              onChange={handleSeek}
              className="flex-1"
            />
            <span className="text-white text-sm">{formatTime(duration)}</span>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <motion.div
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
              >
                <Button
                  onClick={togglePlay}
                  variant="ghost"
                  size="icon"
                  className="text-white hover:bg-[#111111d1] hover:text-white"
                >
                  {isPlaying ? (
                    <Pause className="h-5 w-5" />
                  ) : (
                    <Play className="h-5 w-5" />
                  )}
                </Button>
              </motion.div>
              <div className="flex items-center gap-x-1">
                <motion.div
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                >
                  <Button
                    onClick={toggleMute}
                    variant="ghost"
                    size="icon"
                    className="text-white hover:bg-[#111111d1] hover:text-white"
                  >
                    {isMuted ? (
                      <VolumeX className="h-5 w-5" />
                    ) : volume > 0.5 ? (
                      <Volume2 className="h-5 w-5" />
                    ) : (
                      <Volume1 className="h-5 w-5" />
                    )}
                  </Button>
                </motion.div>

                <div className="w-24">
                  <CustomSlider
                    value={volume * 100}
                    onChange={handleVolumeChange}
                  />
                </div>
              </div>
            </div>

            <div className="flex items-center gap-2">
              {[0.5, 1, 1.5, 2].map((speed) => (
                <motion.div
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  key={speed}
                >
                  <Button
                    onClick={() => setSpeed(speed)}
                    variant="ghost"
                    size="icon"
                    className={cn(
                      "text-white hover:bg-[#111111d1] hover:text-white",
                      playbackSpeed === speed && "bg-[#111111d1]"
                    )}
                  >
                    {speed}x
                  </Button>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  </motion.div>
);
};

export default VideoPlayer;


demo.tsx
import VideoPlayer from "@/components/ui/video-player"

const VideoPlayerDemo = () => {
    return <VideoPlayer src="https://videos.pexels.com/video-files/30333849/13003128_2560_1440_25fps.mp4"/>
}

export { VideoPlayerDemo }
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

Install NPM dependencies:
```bash
lucide-react, framer-motion, @radix-ui/react-slot, class-variance-authority
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

import React, { useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Play, Pause, Volume2, Volume1, VolumeX } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";

const formatTime = (seconds: number) => {
const minutes = Math.floor(seconds / 60);
const remainingSeconds = Math.floor(seconds % 60);
return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`;
};

const CustomSlider = ({
value,
onChange,
className,
}: {
value: number;
onChange: (value: number) => void;
className?: string;
}) => {
return (
  <motion.div
    className={cn(
      "relative w-full h-1 bg-white/20 rounded-full cursor-pointer",
      className
    )}
    onClick={(e) => {
      const rect = e.currentTarget.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const percentage = (x / rect.width) * 100;
      onChange(Math.min(Math.max(percentage, 0), 100));
    }}
  >
    <motion.div
      className="absolute top-0 left-0 h-full bg-white rounded-full"
      style={{ width: `${value}%` }}
      initial={{ width: 0 }}
      animate={{ width: `${value}%` }}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
    />
  </motion.div>
);
};

const VideoPlayer = ({ src }: { src: string }) => {
const videoRef = useRef<HTMLVideoElement>(null);
const [isPlaying, setIsPlaying] = useState(false);
const [volume, setVolume] = useState(1);
const [progress, setProgress] = useState(0);
const [isMuted, setIsMuted] = useState(false);
const [playbackSpeed, setPlaybackSpeed] = useState(1);
const [showControls, setShowControls] = useState(false);
const [currentTime, setCurrentTime] = useState(0);
const [duration, setDuration] = useState(0);

const togglePlay = () => {
  if (videoRef.current) {
    if (isPlaying) {
      videoRef.current.pause();
    } else {
      videoRef.current.play();
    }
    setIsPlaying(!isPlaying);
  }
};

const handleVolumeChange = (value: number) => {
  if (videoRef.current) {
    const newVolume = value / 100;
    videoRef.current.volume = newVolume;
    setVolume(newVolume);
    setIsMuted(newVolume === 0);
  }
};

const handleTimeUpdate = () => {
  if (videoRef.current) {
    const progress =
      (videoRef.current.currentTime / videoRef.current.duration) * 100;
    setProgress(isFinite(progress) ? progress : 0);
    setCurrentTime(videoRef.current.currentTime);
    setDuration(videoRef.current.duration);
  }
};

const handleSeek = (value: number) => {
  if (videoRef.current && videoRef.current.duration) {
    const time = (value / 100) * videoRef.current.duration;
    if (isFinite(time)) {
      videoRef.current.currentTime = time;
      setProgress(value);
    }
  }
};

const toggleMute = () => {
  if (videoRef.current) {
    videoRef.current.muted = !isMuted;
    setIsMuted(!isMuted);
    if (!isMuted) {
      setVolume(0);
    } else {
      setVolume(1);
      videoRef.current.volume = 1;
    }
  }
};

const setSpeed = (speed: number) => {
  if (videoRef.current) {
    videoRef.current.playbackRate = speed;
    setPlaybackSpeed(speed);
  }
};

return (
  <motion.div
    className="relative w-full max-w-4xl mx-auto rounded-xl overflow-hidden bg-[#11111198] shadow-[0_0_20px_rgba(0,0,0,0.2)] backdrop-blur-sm"
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5 }}
    onMouseEnter={() => setShowControls(true)}
    onMouseLeave={() => setShowControls(false)}
  >
    <video
      ref={videoRef}
      className="w-full"
      onTimeUpdate={handleTimeUpdate}
      src={src}
      onClick={togglePlay}
    />

    <AnimatePresence>
      {showControls && (
        <motion.div
          className="absolute bottom-0 mx-auto max-w-xl left-0 right-0 p-4 m-2 bg-[#11111198] backdrop-blur-md rounded-2xl"
          initial={{ y: 20, opacity: 0, filter: "blur(10px)" }}
          animate={{ y: 0, opacity: 1, filter: "blur(0px)" }}
          exit={{ y: 20, opacity: 0, filter: "blur(10px)" }}
          transition={{ duration: 0.6, ease: "circInOut", type: "spring" }}
        >
          <div className="flex items-center gap-2 mb-2">
            <span className="text-white text-sm">
              {formatTime(currentTime)}
            </span>
            <CustomSlider
              value={progress}
              onChange={handleSeek}
              className="flex-1"
            />
            <span className="text-white text-sm">{formatTime(duration)}</span>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <motion.div
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
              >
                <Button
                  onClick={togglePlay}
                  variant="ghost"
                  size="icon"
                  className="text-white hover:bg-[#111111d1] hover:text-white"
                >
                  {isPlaying ? (
                    <Pause className="h-5 w-5" />
                  ) : (
                    <Play className="h-5 w-5" />
                  )}
                </Button>
              </motion.div>
              <div className="flex items-center gap-x-1">
                <motion.div
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                >
                  <Button
                    onClick={toggleMute}
                    variant="ghost"
                    size="icon"
                    className="text-white hover:bg-[#111111d1] hover:text-white"
                  >
                    {isMuted ? (
                      <VolumeX className="h-5 w-5" />
                    ) : volume > 0.5 ? (
                      <Volume2 className="h-5 w-5" />
                    ) : (
                      <Volume1 className="h-5 w-5" />
                    )}
                  </Button>
                </motion.div>

                <div className="w-24">
                  <CustomSlider
                    value={volume * 100}
                    onChange={handleVolumeChange}
                  />
                </div>
              </div>
            </div>

            <div className="flex items-center gap-2">
              {[0.5, 1, 1.5, 2].map((speed) => (
                <motion.div
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  key={speed}
                >
                  <Button
                    onClick={() => setSpeed(speed)}
                    variant="ghost"
                    size="icon"
                    className={cn(
                      "text-white hover:bg-[#111111d1] hover:text-white",
                      playbackSpeed === speed && "bg-[#111111d1]"
                    )}
                  >
                    {speed}x
                  </Button>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  </motion.div>
);
};

export default VideoPlayer;
