import React from 'react'
import { FiArrowRight } from 'react-icons/fi'

type ButtonVariant = 'solid' | 'outline'
type ButtonColor = 'primary' | 'white'

interface ButtonBaseProps {
  value: string
  variant?: ButtonVariant
  color?: ButtonColor
  icon?: boolean
}

export type ButtonProps = ButtonBaseProps & React.ButtonHTMLAttributes<HTMLButtonElement>

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ value, variant = 'solid', color = 'primary', icon = true, className = '', ...props }, ref) => {
    const baseStyles = 'px-6 py-3 rounded-lg font-medium transition-colors'
    const solidStyles = color === 'primary' 
      ? 'bg-blue-500 hover:bg-blue-600 text-white' 
      : 'bg-white hover:bg-gray-100 text-gray-900'
    const outlineStyles = color === 'primary'
      ? 'border-2 border-blue-500 text-blue-500 hover:bg-blue-500/10'
      : 'border-2 border-white text-white hover:bg-white/10'
    
    const buttonStyles = `${baseStyles} ${variant === 'solid' ? solidStyles : outlineStyles} ${
      props.disabled ? 'opacity-50 cursor-not-allowed' : ''
    } ${className}`

    return (
      <button
        ref={ref}
        className={buttonStyles}
        {...props}
      >
        <div className="flex items-center gap-2">
          {value}
          {icon && <FiArrowRight />}
        </div>
      </button>
    )
  }
)

Button.displayName = 'Button'

export default Button 