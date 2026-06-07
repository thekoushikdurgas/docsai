<https://21st.dev/community/components/itsankitverma/otp-input/default>
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
otp-input.tsx
import { PinInput } from '@ark-ui/react/pin-input'

export const Basic = () => {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 dark:bg-gray-900 p-6 w-full">
      <div className="max-w-md w-full space-y-6 rounded-2xl bg-white dark:bg-gray-800 shadow-lg p-8 text-center">
        
        {/* Title and Description */}
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Enter Your Verification Code
          </h2>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            We’ve sent a 4-digit code to your email. Please enter it below to continue.
          </p>
        </div>

        {/* PIN Input */}
        <PinInput.Root
          onValueComplete={(e) => alert(`Entered: ${e.valueAsString}`)}
        >
          <PinInput.Label className="sr-only">Verification Code</PinInput.Label>
          <PinInput.Control className="flex justify-center gap-4">
            {[0, 1, 2, 3].map((id, index) => (
              <PinInput.Input
                key={id}
                index={index}
                className="w-12 h-14 text-center text-xl font-semibold 
                           border-b-2 border-gray-400 dark:border-gray-500 
                           bg-transparent text-gray-900 dark:text-white 
                           focus:border-blue-500 dark:focus:border-blue-400 
                           focus:ring-0 outline-none 
                           transition-all duration-200"
              />
            ))}
          </PinInput.Control>
          <PinInput.HiddenInput />
        </PinInput.Root>

        {/* Extra Info */}
        <div className="text-sm text-gray-500 dark:text-gray-400">
          Didn’t receive the code?{" "}
          <span className="text-blue-600 dark:text-blue-400 cursor-pointer hover:underline">
            Resend
          </span>
        </div>
      </div>
    </div>
  )
}


demo.tsx
import { Basic } from "@/components/ui/otp-input";

export default function DemoOne() {
  return <Basic />;
}

```

Install NPM dependencies:

```bash
@ark-ui/react
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
import { PinInput } from '@ark-ui/react/pin-input'

export const Basic = () => {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 dark:bg-gray-900 p-6 w-full">
      <div className="max-w-md w-full space-y-6 rounded-2xl bg-white dark:bg-gray-800 shadow-lg p-8 text-center">

        {/* Title and Description */}
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Enter Your Verification Code
          </h2>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            We’ve sent a 4-digit code to your email. Please enter it below to continue.
          </p>
        </div>

        {/* PIN Input */}
        <PinInput.Root
          onValueComplete={(e) => alert(`Entered: ${e.valueAsString}`)}
        >
          <PinInput.Label className="sr-only">Verification Code</PinInput.Label>
          <PinInput.Control className="flex justify-center gap-4">
            {[0, 1, 2, 3].map((id, index) => (
              <PinInput.Input
                key={id}
                index={index}
                className="w-12 h-14 text-center text-xl font-semibold 
                           border-b-2 border-gray-400 dark:border-gray-500 
                           bg-transparent text-gray-900 dark:text-white 
                           focus:border-blue-500 dark:focus:border-blue-400 
                           focus:ring-0 outline-none 
                           transition-all duration-200"
              />
            ))}
          </PinInput.Control>
          <PinInput.HiddenInput />
        </PinInput.Root>

        {/* Extra Info */}
        <div className="text-sm text-gray-500 dark:text-gray-400">
          Didn’t receive the code?{" "}
          <span className="text-blue-600 dark:text-blue-400 cursor-pointer hover:underline">
            Resend
          </span>
        </div>
      </div>
    </div>
  )
}
