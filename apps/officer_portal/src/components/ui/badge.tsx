import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'pending' | 'verified' | 'neutral' | 'outline';
}

export const Badge: React.FC<BadgeProps> = ({
  className,
  variant = 'neutral',
  children,
  ...props
}) => {
  const baseStyles =
    'inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold tracking-wide transition-colors';

  const variants = {
    pending: 'bg-amber-100 text-amber-800 border border-amber-300',
    verified: 'bg-emerald-100 text-emerald-800 border border-emerald-300',
    neutral: 'bg-slate-100 text-slate-700 border border-slate-200',
    outline: 'border border-slate-300 text-slate-600',
  };

  return (
    <div className={twMerge(clsx(baseStyles, variants[variant], className))} {...props}>
      {variant === 'pending' && <span className="h-1.5 w-1.5 rounded-full bg-amber-600 animate-pulse" />}
      {variant === 'verified' && <span className="h-1.5 w-1.5 rounded-full bg-emerald-600" />}
      {children}
    </div>
  );
};
