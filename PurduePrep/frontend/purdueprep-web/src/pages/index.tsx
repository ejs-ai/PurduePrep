import { useState } from 'react';

const Home: React.FC = () => {
  const [inputValue, setInputValue] = useState<string>('');

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  return (
    <div>
      <h1>Text Input Example</h1>
      <input 
        type="text" 
        value={inputValue} 
        onChange={handleInputChange} 
        placeholder="Type something here..." 
      />
      <p>You typed: {inputValue}</p>
    </div>
  );
};

export default Home;
