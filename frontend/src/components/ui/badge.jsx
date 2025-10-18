import * as React from 'react';
import { cva } from 'class-variance-authority';

const badgeVariants = cva(
  'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        default:
          'border-transparent bg-primary text-primary-foreground hover:opacity-90',
        secondary:
          'border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80',
        destructive:
          'border-transparent bg-destructive text-destructive-foreground hover:opacity-90',
        outline: 'text-foreground border-border',
        success: 'border-transparent bg-success text-white',
        premium: 'bg-gradient-to-r from-primary to-primary-glow text-primary-foreground border-0',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

export const Badge = ({ className, variant, ...props }) => {
  return (
    <div className={`${badgeVariants({ variant })} ${className || ''}`} {...props} />
  );
};