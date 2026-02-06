/**
 * Text input form for symptom assessment
 */
import { useState } from 'react';
import { Button } from '../common/Button';

const EXAMPLE_TEXT = `I've been feeling really down for the past few weeks. I can't seem to enjoy anything anymore, not even activities I used to love. I'm having trouble sleeping at night - I lie awake for hours. During the day, I feel completely exhausted and have no energy to do anything. I've lost my appetite and dropped about 10 pounds. I feel worthless and guilty about everything, even things that aren't my fault. It's hard to concentrate at work, and I can't make simple decisions. I just feel like there's no point to anything.`;

export const TextInputForm = ({ onSubmit, isLoading }) => {
  const [text, setText] = useState('');
  const [charCount, setCharCount] = useState(0);
  const maxChars = 5000;
  const minChars = 10;

  const handleChange = (e) => {
    const value = e.target.value;
    setText(value);
    setCharCount(value.length);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim().length >= minChars && text.length <= maxChars) {
      onSubmit(text);
    }
  };

  const handleUseExample = () => {
    setText(EXAMPLE_TEXT);
    setCharCount(EXAMPLE_TEXT.length);
  };

  const handleClear = () => {
    setText('');
    setCharCount(0);
  };

  const isValid = text.trim().length >= minChars && text.length <= maxChars;

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="symptom-text" className="block text-sm font-medium text-gray-700 mb-2">
          Describe patient symptoms in natural language
        </label>

        <textarea
          id="symptom-text"
          value={text}
          onChange={handleChange}
          placeholder="Enter a detailed description of the patient's symptoms, including mood, sleep patterns, energy levels, interests, appetite, concentration, and any other relevant observations..."
          className="w-full h-48 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none"
          maxLength={maxChars}
          disabled={isLoading}
        />

        <div className="flex justify-between items-center mt-2 text-sm">
          <span className={`${charCount < minChars ? 'text-red-600' : 'text-gray-500'}`}>
            {charCount < minChars
              ? `Minimum ${minChars} characters (${minChars - charCount} more needed)`
              : `${charCount} / ${maxChars} characters`}
          </span>

          <div className="space-x-2">
            <button
              type="button"
              onClick={handleUseExample}
              className="text-primary-600 hover:text-primary-700 font-medium"
              disabled={isLoading}
            >
              Use Example
            </button>
            <button
              type="button"
              onClick={handleClear}
              className="text-gray-600 hover:text-gray-700 font-medium"
              disabled={isLoading || charCount === 0}
            >
              Clear
            </button>
          </div>
        </div>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="font-medium text-blue-900 mb-2">💡 Input Guidelines</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Describe symptoms in free-form natural language</li>
          <li>• Include duration information (e.g., "for 3 weeks", "past month")</li>
          <li>• Mention functional impairment (e.g., "can't work", "stopped socializing")</li>
          <li>• Be specific about frequency (e.g., "every day", "most days")</li>
        </ul>
      </div>

      <Button
        type="submit"
        variant="primary"
        size="lg"
        disabled={!isValid || isLoading}
        isLoading={isLoading}
        className="w-full"
      >
        Analyze Symptoms
      </Button>
    </form>
  );
};
