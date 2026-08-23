import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function Card({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={twMerge(
        clsx(
          'rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs transition-shadow hover:shadow-sm',
          className
        )
      )}
      {...props}
    >
      {children}
    </div>
  );
}
