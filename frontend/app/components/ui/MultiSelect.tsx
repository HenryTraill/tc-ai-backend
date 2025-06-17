import React, { useState, useRef, useEffect } from 'react';

interface Option {
  id: string | number;
  label: string;
}

interface MultiSelectProps {
  options: Option[];
  value: (string | number)[];
  onChange: (value: (string | number)[]) => void;
  placeholder?: string;
  className?: string;
  disabled?: boolean;
}

export const MultiSelect: React.FC<MultiSelectProps> = ({
  options,
  value,
  onChange,
  placeholder = "Select options...",
  className = "",
  disabled = false
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const dropdownRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
        setSearchTerm("");
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Filter options based on search term
  const filteredOptions = options.filter(option =>
    option.label.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Get selected options for display - fix the comparison logic
  const selectedOptions = options.filter(option => {
    const valueAsStrings = value.map(v => String(v));
    return valueAsStrings.includes(String(option.id));
  });

  const handleToggleOption = (optionId: string | number) => {
    const valueAsStrings = value.map(v => String(v));
    const optionIdStr = String(optionId);

    if (valueAsStrings.includes(optionIdStr)) {
      // Remove the option - preserve original type
      onChange(value.filter(id => String(id) !== optionIdStr));
    } else {
      // Add the option - preserve original type from options
      onChange([...value, optionId]);
    }
  };

  const handleRemoveOption = (optionId: string | number, e: React.MouseEvent) => {
    e.stopPropagation();
    onChange(value.filter(id => String(id) !== String(optionId)));
  };

  const handleClearAll = (e: React.MouseEvent) => {
    e.stopPropagation();
    onChange([]);
  };

  // Helper function to check if an option is selected
  const isOptionSelected = (optionId: string | number) => {
    const valueAsStrings = value.map(v => String(v));
    return valueAsStrings.includes(String(optionId));
  };

  return (
    <div className={`relative ${className}`} ref={dropdownRef}>
      {/* Main input/trigger */}
      <div
        className={`
          min-h-[46px] w-full px-3 py-2 border border-navy-blue rounded-lg
          bg-grey cursor-pointer flex items-center gap-2 flex-wrap
          ${disabled ? 'bg-gray-50 cursor-not-allowed border-gray-300' : ''}
          ${isOpen ? 'border-blue-500' : ''}
        `}
        onClick={() => !disabled && setIsOpen(!isOpen)}
      >
        {/* Selected items */}
        {selectedOptions.length > 0 ? (
          <div className="flex flex-wrap gap-2 flex-1">
            {selectedOptions.map(option => (
              <span
                key={option.id}
                className="inline-flex items-center gap-2 px-3 py-1 bg-sky-blue text-white text-xs rounded-full font-medium"
              >
                {option.label}
                {!disabled && (
                  <button
                    type="button"
                    onClick={(e) => handleRemoveOption(option.id, e)}
                    className="hover:bg-sky-blue rounded-full p-0.5 transition-colors"
                  >
                    <i className="fas fa-times text-xs"></i>
                  </button>
                )}
              </span>
            ))}
          </div>
        ) : (
          <span className="text-gray-400 flex-1 text-sm">{placeholder}</span>
        )}

        {/* Clear all button */}
        {selectedOptions.length > 0 && !disabled && (
          <button
            type="button"
            onClick={handleClearAll}
            className="text-gray-400 hover:text-gray-600 p-1 transition-colors"
          >
            <i className="fas fa-times"></i>
          </button>
        )}

        {/* Dropdown arrow */}
        <i className={`fas fa-chevron-up text-gray-400 transition-transform ${isOpen ? '' : 'rotate-180'}`}></i>
      </div>

      {/* Dropdown */}
      {isOpen && !disabled && (
        <div className="absolute z-50 w-full mt-2 bg-white border border-gray-200 rounded-lg shadow-lg overflow-hidden">
          {/* Search input */}
          <div className="p-4 border-b border-gray-100">
            <input
              ref={inputRef}
              type="text"
              placeholder="Search..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-4 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              autoFocus
            />
          </div>

          {/* Options list */}
          <div className="max-h-64 overflow-y-auto">
            {filteredOptions.length > 0 ? (
              filteredOptions.map(option => {
                const isSelected = isOptionSelected(option.id);
                return (
                  <div
                    key={option.id}
                    className={`
                      px-4 py-3 cursor-pointer flex items-center gap-3 hover:bg-gray-50 transition-colors
                      ${isSelected ? 'bg-blue-50 border-l-4 border-blue-500' : ''}
                    `}
                    onClick={() => handleToggleOption(option.id)}
                  >
                    {/* Custom checkbox */}
                    <div className={`
                      w-5 h-5 rounded border-2 flex items-center justify-center transition-all
                      ${isSelected
                        ? 'bg-blue-500 border-blue-500'
                        : 'border-gray-300 hover:border-blue-400'
                      }
                    `}>
                      {isSelected && (
                        <i className="fas fa-check text-white text-xs"></i>
                      )}
                    </div>

                    <span className={`flex-1 text-sm ${isSelected ? 'text-blue-700 font-medium' : 'text-gray-700'}`}>
                      {option.label}
                    </span>
                  </div>
                );
              })
            ) : (
              <div className="px-4 py-8 text-gray-500 text-sm text-center">
                No options found
              </div>
            )}
          </div>

          {/* Footer with selection count */}
          {selectedOptions.length > 0 && (
            <div className="px-4 py-3 border-t border-gray-100 bg-gray-50">
              <span className="text-xs text-gray-600">
                {selectedOptions.length} student{selectedOptions.length !== 1 ? 's' : ''} selected
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};