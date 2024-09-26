import { useState } from 'react';

const Home: React.FC = () => {
  const [inputValue, setInputValue] = useState<string>('');
  const [responseMessage, setResponseMessage] = useState<string>('');

  // Handle input change
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  // Send input to Flask backend
  const handleSubmit = async () => {
    try {
      const response = await fetch('/api/receive-text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ inputText: inputValue }),  // Send input value as JSON
      });

      const data = await response.json();
      setResponseMessage(data.message);  // Set the message returned from Flask

    } catch (error) {
      console.error('Error sending text to backend:', error);
      setResponseMessage('Error communicating with backend');
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Please Input Your Class Content (text only for now)</h1>
      <textarea
        value={inputValue}
        onChange={handleInputChange}
        placeholder="Type something here..."
        style={styles.textarea}
        wrap="soft"  // Use "hard" if you want line breaks in the submitted value
      />
      <button onClick={handleSubmit} style={styles.submitButton}>Submit</button>

      {responseMessage && <p>Response from backend: {responseMessage}</p>}
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column' as 'column',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh', // Full viewport height
    backgroundColor: '#f0f0f0', // Light gray background for better contrast
  },
  title: {
    fontSize: '2rem', // Larger title font size
    marginBottom: '20px',
  },
  textarea: {
    width: '400px',
    height: '300px',  // Taller input box for multiple lines
    padding: '10px',
    fontSize: '1.2rem',
    borderRadius: '8px',
    border: '2px solid #ccc',
    marginBottom: '20px',
    resize: 'vertical',  // Allow resizing vertically
    overflowWrap: 'break-word',  // Ensure words break correctly
  },
  submitButton: {
    padding: '10px 20px', // Button padding
    fontSize: '1.2rem', // Larger font size for the button
    backgroundColor: '#0070f3', // Next.js blue color
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
  },
};

export default Home;
