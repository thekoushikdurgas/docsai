https://21st.dev/community/components/ayushmxxn/typewriter-testimonial/default
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
typewriter-testimonial.tsx
'use client';
import React, { useState, useEffect, useRef, useCallback } from 'react'; // Added useCallback
import { motion, AnimatePresence } from 'framer-motion';

type Testimonial = {
  image: string;
  audio: string;
  text: string;
  name: string;
  jobtitle: string;
};

type ComponentProps = {
  testimonials: Testimonial[];
};

export const Component: React.FC<ComponentProps> = ({ testimonials }) => {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  const audioPlayerRef = useRef<HTMLAudioElement | null>(null); 
  const [hasBeenHovered, setHasBeenHovered] = useState<boolean[]>(new Array(testimonials.length).fill(false));
  const [typedText, setTypedText] = useState('');
  const typewriterTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const currentTextRef = useRef('');

  const stopAudio = useCallback(() => {
    if (audioPlayerRef.current) {
      audioPlayerRef.current.pause(); 
      audioPlayerRef.current.currentTime = 0; 
      audioPlayerRef.current.src = ''; 
      audioPlayerRef.current.load(); 
      audioPlayerRef.current = null; 
    }
  }, []); 

  const startTypewriter = useCallback((text: string) => {
    if (typewriterTimeoutRef.current) {
      clearTimeout(typewriterTimeoutRef.current);
    }
    setTypedText('');
    currentTextRef.current = text;
    
    let i = 0;
    const type = () => {
      if (i <= text.length) {
        setTypedText(text.slice(0, i));
        i++;
        typewriterTimeoutRef.current = setTimeout(type, 50);
      }
    };
    type();
  }, []);
  const stopTypewriter = useCallback(() => {
    if (typewriterTimeoutRef.current) {
      clearTimeout(typewriterTimeoutRef.current);
      typewriterTimeoutRef.current = null;
    }
    setTypedText('');
    currentTextRef.current = '';
  }, []); 
  const handleMouseEnter = useCallback((index: number) => {
    
    stopAudio(); 

    setHoveredIndex(index);
  
    const newAudio = new Audio(`/audio/${testimonials[index].audio}`);
    audioPlayerRef.current = newAudio; 
    newAudio.play().catch(e => {
        console.warn("Audio playback prevented or failed:", e);
      
    });
    
    setHasBeenHovered(prev => {
      const updated = [...prev];
      updated[index] = true;
      return updated;
    });
    startTypewriter(testimonials[index].text);
  }, [testimonials, stopAudio, startTypewriter]); 

  
  const handleMouseLeave = useCallback(() => {
    stopAudio(); 
    setHoveredIndex(null);
    stopTypewriter();
  }, [stopAudio, stopTypewriter]);
  useEffect(() => {
    return () => {
      stopAudio(); 
      stopTypewriter(); 
    };
  }, [stopAudio, stopTypewriter]); 

  return (
    <div className="flex justify-center items-center gap-4 flex-wrap">
      {testimonials.map((testimonial, index) => (
        <motion.div
          key={index}
          className="relative flex flex-col items-center"
          onMouseEnter={() => handleMouseEnter(index)} 
          onMouseLeave={handleMouseLeave}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <motion.img
            src={testimonial.image}
            alt={`Testimonial ${index}`}
            className="w-16 h-16 rounded-full border-4 hover:animate-pulse border-gray-300"
            animate={{ 
              borderColor: (hoveredIndex === index || hasBeenHovered[index]) ? '#ACA0FB' : '#E5E7EB'
            }}
            transition={{ duration: 0.3 }}
          />
          <AnimatePresence>
            {hoveredIndex === index && (
              <motion.div
                initial={{ opacity: 0, scale: 0.8, y: -10 }}
                animate={{ opacity: 1, scale: 1, y: -20 }}
                exit={{ opacity: 0, scale: 0.8, y: -10 }}
                transition={{ duration: 0.4 }}
                className="absolute bottom-20 bg-white text-black text-sm px-4 py-3 rounded-lg shadow-2xl max-w-xs w-56"
              >
                <div className="h-24 overflow-hidden whitespace-pre-wrap">
                  {typedText}
                  <span className="animate-blink">|</span>
                </div>
                <p className="mt-2 text-right font-semibold">{testimonial.name}</p>
                <p className="text-right text-gray-500 text-sm">{testimonial.jobtitle}</p>
                <div className="absolute left-1/2 transform -translate-x-1/2 -bottom-4">
                  <div className="w-3 h-3 bg-white rounded-full shadow-lg"></div>
                  <div className="w-2 h-2 bg-white rounded-full shadow-lg mt-1"></div>
                  <div className="w-1 h-1 bg-white rounded-full shadow-lg mt-1"></div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      ))}
    </div>
  );
};

demo.tsx
// This is a demo of a preview
'use client';
import { Component } from "@/components/ui/typewriter-testimonial";

const DemoOne = () => {
  const testimonials = [
    {
      image: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?q=80&w=1780&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
      audio: 'audio_1.mp3',
      text: 'This product has revolutionized my workflow. The intuitive interface and powerful features make it an indispensable tool for my daily tasks. Highly recommended for anyone looking to boost productivity.',
      name: 'John Doe',
      jobtitle: 'Software Engineer',
    },
    {
      image: 'https://images.unsplash.com/photo-1527980965255-d3b416303d12?q=80&w=1780&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
      audio: 'audio_2.mp3',
      text: 'An exceptional experience from start to finish. The customer support is top-notch, and the product consistently exceeds my expectations. I can confidently say this is the best in its class.',
      name: 'Jane Smith',
      jobtitle: 'Marketing Manager',
    },
    {
      image: 'https://images.unsplash.com/photo-1633332755192-727a05c4013d?q=80&w=1780&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
      audio: 'audio_3.mp3',
      text: 'The design is sleek, and the performance is unparalleled. It truly stands out among competitors. This investment has paid off exponentially in terms of efficiency and results.',
      name: 'Alex Johnson',
      jobtitle: 'UX Designer',
    },
    {
      image: 'https://images.unsplash.com/photo-1586297135537-94bc9ba060aa?q=80&w=1780&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
      audio: 'audio_4.mp3',
      text: 'I was skeptical at first, but this product delivered beyond my wildest dreams. It is robust, reliable, and has become an essential part of my professional toolkit. Simply amazing!',
      name: 'Emily White',
      jobtitle: 'Project Lead',
    },
    {
      image: 'https://images.unsplash.com/photo-1507003211169-0a6dd7228f2d?q=80&w=1780&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
      audio: 'audio_5.mp3',
      text: 'This tool is a game-changer for data analysis. The visualisations are clear, and the insights gained are invaluable. It has transformed how we approach our business decisions.',
      name: 'David Lee',
      jobtitle: 'Data Scientist',
    },
    {
      image: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=1780&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
      audio: 'audio_6.mp3',
      text: 'I appreciate the continuous updates and improvements. The team behind this product clearly listens to user feedback. It keeps getting better with every release. Fantastic!',
      name: 'Sarah Chen',
      jobtitle: 'Operations Manager',
    },
    {
      image: 'https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?q=80&w=1780&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
      audio: 'audio_7.mp3',
      text: 'The support I received was outstanding. They quickly resolved my issue and went above and beyond. It is comforting to know such dedicated professionals are behind this software.',
      name: 'Michael Brown',
      jobtitle: 'Customer Support Lead',
    },
    {
      image: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=1780&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
      audio: 'audio_8.mp3',
      text: 'This is exactly what I needed! It simplified complex tasks and allowed me to focus on what truly matters. The seamless integration with my existing tools was a huge plus.',
      name: 'Chris Taylor',
      jobtitle: 'Entrepreneur',
    },
  ];

  return (
    <div className="flex w-full h-screen justify-center items-center">
      <Component testimonials={testimonials} />
    </div>
  );
};

export default DemoOne;
```

Install NPM dependencies:
```bash
framer-motion
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
'use client';
import React, { useState, useEffect, useRef, useCallback } from 'react'; // Added useCallback
import { motion, AnimatePresence } from 'framer-motion';

type Testimonial = {
  image: string;
  audio: string;
  text: string;
  name: string;
  jobtitle: string;
};

type ComponentProps = {
  testimonials: Testimonial[];
};

export const Component: React.FC<ComponentProps> = ({ testimonials }) => {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  const audioPlayerRef = useRef<HTMLAudioElement | null>(null); 
  const [hasBeenHovered, setHasBeenHovered] = useState<boolean[]>(new Array(testimonials.length).fill(false));
  const [typedText, setTypedText] = useState('');
  const typewriterTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const currentTextRef = useRef('');

  const stopAudio = useCallback(() => {
    if (audioPlayerRef.current) {
      audioPlayerRef.current.pause(); 
      audioPlayerRef.current.currentTime = 0; 
      audioPlayerRef.current.src = ''; 
      audioPlayerRef.current.load(); 
      audioPlayerRef.current = null; 
    }
  }, []); 

  const startTypewriter = useCallback((text: string) => {
    if (typewriterTimeoutRef.current) {
      clearTimeout(typewriterTimeoutRef.current);
    }
    setTypedText('');
    currentTextRef.current = text;
    
    let i = 0;
    const type = () => {
      if (i <= text.length) {
        setTypedText(text.slice(0, i));
        i++;
        typewriterTimeoutRef.current = setTimeout(type, 50);
      }
    };
    type();
  }, []);
  const stopTypewriter = useCallback(() => {
    if (typewriterTimeoutRef.current) {
      clearTimeout(typewriterTimeoutRef.current);
      typewriterTimeoutRef.current = null;
    }
    setTypedText('');
    currentTextRef.current = '';
  }, []); 
  const handleMouseEnter = useCallback((index: number) => {
    
    stopAudio(); 

    setHoveredIndex(index);
  
    const newAudio = new Audio(`/audio/${testimonials[index].audio}`);
    audioPlayerRef.current = newAudio; 
    newAudio.play().catch(e => {
        console.warn("Audio playback prevented or failed:", e);
      
    });
    
    setHasBeenHovered(prev => {
      const updated = [...prev];
      updated[index] = true;
      return updated;
    });
    startTypewriter(testimonials[index].text);
  }, [testimonials, stopAudio, startTypewriter]); 

  
  const handleMouseLeave = useCallback(() => {
    stopAudio(); 
    setHoveredIndex(null);
    stopTypewriter();
  }, [stopAudio, stopTypewriter]);
  useEffect(() => {
    return () => {
      stopAudio(); 
      stopTypewriter(); 
    };
  }, [stopAudio, stopTypewriter]); 

  return (
    <div className="flex justify-center items-center gap-4 flex-wrap">
      {testimonials.map((testimonial, index) => (
        <motion.div
          key={index}
          className="relative flex flex-col items-center"
          onMouseEnter={() => handleMouseEnter(index)} 
          onMouseLeave={handleMouseLeave}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <motion.img
            src={testimonial.image}
            alt={`Testimonial ${index}`}
            className="w-16 h-16 rounded-full border-4 hover:animate-pulse border-gray-300"
            animate={{ 
              borderColor: (hoveredIndex === index || hasBeenHovered[index]) ? '#ACA0FB' : '#E5E7EB'
            }}
            transition={{ duration: 0.3 }}
          />
          <AnimatePresence>
            {hoveredIndex === index && (
              <motion.div
                initial={{ opacity: 0, scale: 0.8, y: -10 }}
                animate={{ opacity: 1, scale: 1, y: -20 }}
                exit={{ opacity: 0, scale: 0.8, y: -10 }}
                transition={{ duration: 0.4 }}
                className="absolute bottom-20 bg-white text-black text-sm px-4 py-3 rounded-lg shadow-2xl max-w-xs w-56"
              >
                <div className="h-24 overflow-hidden whitespace-pre-wrap">
                  {typedText}
                  <span className="animate-blink">|</span>
                </div>
                <p className="mt-2 text-right font-semibold">{testimonial.name}</p>
                <p className="text-right text-gray-500 text-sm">{testimonial.jobtitle}</p>
                <div className="absolute left-1/2 transform -translate-x-1/2 -bottom-4">
                  <div className="w-3 h-3 bg-white rounded-full shadow-lg"></div>
                  <div className="w-2 h-2 bg-white rounded-full shadow-lg mt-1"></div>
                  <div className="w-1 h-1 bg-white rounded-full shadow-lg mt-1"></div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      ))}
    </div>
  );
};