export const Chip = ({ children, variant = 'default', size = 'md', className = '', ...props }) => {
    const baseStyles = 'inline-flex items-center gap-1.5 font-medium rounded-full border transition-all duration-200';

    const variants = {
        strength: 'bg-baby-blue text-navy-blue border-sky-blue hover:bg-sky-blue hover:text-white',
        focus: 'bg-light-blue text-navy-blue border-steel-blue hover:bg-steel-blue hover:text-white',
        default: 'bg-white text-navy-blue border-steel-blue hover:bg-steel-blue hover:text-white'
    };

    const sizes = {
        sm: 'px-2.5 py-1 text-xs',
        md: 'px-3 py-1.5 text-sm',
        lg: 'px-4 py-2 text-base'
    };

    return (
        <span
            className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
            {...props}
        >
            {variant === 'strength' && <div className="w-1.5 h-1.5 bg-sky-blue rounded-full"></div>}
            {variant === 'focus' && <div className="w-1.5 h-1.5 bg-steel-blue rounded-full"></div>}
            {children}
        </span>
    );
};