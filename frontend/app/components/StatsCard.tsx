interface StatsCardProps {
  title: string;
  value: number;
  description: string;
  trend: {
    type: "up" | "down",
    label: string
  }
}

export const StatsCard = ({ title, value, description, trend }: StatsCardProps) => {
  return (
    <div className="bg-white border border-navy-blue-15 rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 relative overflow-hidden group">
      <h3 className="text-sm font-semibold text-navy-blue-75 uppercase tracking-wide mb-4">
        {title}
      </h3>

      <p className="text-4xl font-bold text-dark-blue mb-3 bg-gradient-to-r from-dark-blue to-steel-blue bg-clip-text text-transparent">
        {value}
      </p>

      <p className="text-sm font-medium text-navy-blue-50 mb-3">
        {description}
      </p>

      {trend && (
        <div className={`inline-flex items-center gap-1 text-xs font-semibold px-2 py-1 rounded-lg mt-2 ${trend.type === 'up'
          ? 'bg-green-50 text-green-600'
          : trend.type === 'down'
            ? 'bg-red-50 text-red-600'
            : 'bg-navy-blue-15 text-navy-blue-75'
          }`}>
          {trend.type === 'up' && (
            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M3.293 9.707a1 1 0 010-1.414l6-6a1 1 0 011.414 0l6 6a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L4.707 9.707a1 1 0 01-1.414 0z" clipRule="evenodd"></path>
            </svg>
          )}
          {trend.type === 'down' && (
            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M16.707 10.293a1 1 0 010 1.414l-6 6a1 1 0 01-1.414 0l-6-6a1 1 0 111.414-1.414L9 14.586V3a1 1 0 012 0v11.586l4.293-4.293a1 1 0 011.414 0z" clipRule="evenodd"></path>
            </svg>
          )}
          {trend.label}
        </div>
      )}
    </div>
  )
}