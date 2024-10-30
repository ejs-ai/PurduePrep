import Image from 'next/image';
import { useState, useEffect } from 'react';

interface QuestionData {
  question: string;
  url: string;
}

const Home: React.FC = () => {
  const [inputText, setInputText] = useState<string>('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [questions, setQuestions] = useState<QuestionData[]>([]);  // For questions and URLs
  const [error, setError] = useState<string | null>(null);  // For error handling
  const [loading, setLoading] = useState<boolean>(false);
  const [timeoutReached, setTimeoutReached] = useState<boolean>(false); // To control error timeout

  // Handle input via text or file
  const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>): void => {
    setInputText(event.target.value);
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const file = event.target.files?.[0] || null;
    setSelectedFile(file);
  };

  // Send input to Flask backend
  const handleSubmit = async () => {
    try {
      const response = await fetch('/api/receive-text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ inputText: inputText }),  // Send input value as JSON
      });
  
      const data = await response.json();
  
      // Check if the backend response is successful
      if (data.message === 'Text received successfully') {
        // Fetch questions again after successful input submission
        fetchQuestions();  // Refetch questions from the backend
      } else {
        setError('Failed to submit input.');
      }
    } catch (error) {
      console.error('Error sending text to backend:', error);
      setError('Error communicating with backend.');
    }
  };

  // Fetch questions from the Flask backend
  const fetchQuestions = async () => {
    setLoading(true);  // Start loading when request starts
    setError(null);  // Clear any previous errors
  
    // Set a timeout to show an error message after 5 seconds if nothing happens
    const errorTimeout = setTimeout(() => {
      setTimeoutReached(true); // Flag that we have hit the timeout
      setError('Failed to load questions.');  // Show error after timeout
    }, 60000);  // 60 seconds delay
  
    try {
      const response = await fetch('http://127.0.0.1:5328/api/get-questions');  // Adjust URL based on your setup
      const data = await response.json();
  
      if (response.ok) {
        setQuestions(data.questions);  // Set questions from backend
        setLoading(false);  // End loading state
        clearTimeout(errorTimeout);  // Clear the timeout since we got a successful response
        setTimeoutReached(false); // Reset timeout flag
      } else {
        setError('Failed to load questions.');
      }
    } catch (error) {
      console.error('Error fetching questions:', error);
      if (!timeoutReached) {
        setError('Failed to load questions.');
      }
    } finally {
      setLoading(false);  // End loading regardless of success/failure
    }
  };

  useEffect(() => {
    fetchQuestions();
  }, []);

  return (
    <div style={styles.container}>
      <div style={styles.logoContainer}>
        <Image
          src="/images/ece-logo.jpg" // Path relative to the public directory
          alt="ECE Logo"
          width={100} // Adjust the width as needed
          height={50} // Adjust the height as needed
        />
      </div>
      <h1 style={styles.title}>PurduePrep Beta!</h1>
      <p style={styles.explanation}>PurduePrep finds real exam questions from universities to match your text or document input. We recommend inputting course notes!</p>
      <div style={styles.columns}>
      
        {/* Left Column for Input */}
        <div style={styles.leftColumn}>
          <h2 style={styles.subheader}>Input (text, .txt, or .pdf):</h2>
          <textarea
            value={inputText}
            onChange={handleInputChange}
            placeholder="Type something here..."
            style={styles.textarea}
            wrap="soft"
          />
          <br />
          <input type="file" onChange={handleFileChange} />
          <br />
          <button onClick={handleSubmit} style={styles.submitButton}>Submit</button>
        </div>

        {/* Right Column for Questions */}
        <div style={styles.rightColumn}>
          <h2 style={styles.subheader}>Practice Questions:</h2>
          {loading && <p>Loading questions...</p>}  {/* Show loading state */}
          {timeoutReached && error && <p style={styles.error}>{error}</p>}  {/* Show error only after timeout */}
          <div style={styles.questionContainer}>
          {questions && questions.length > 0 ? (
            questions.map((q, index) => (
              <div key={index} style={styles.questionBlock}>
                <div style={styles.questionCard}>
                  <h3 style={styles.questionText}>{q.question}</h3>
                  <a href={q.url} target="_blank" rel="noopener noreferrer" style={styles.urlText}>
                    {q.url}
                  </a>
                </div>
              </div>
            ))
          ) : !loading ? (
            <p>No questions available</p>
          ) : null}
          </div>
        </div>
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    display: 'flex' as const,
    flexDirection: 'column' as const,
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    background: 'linear-gradient(135deg, #1a1a1a, #333333)',  // Black to gray gradient
    color: '#FFED89',  // Gold text
    fontFamily: '"Cantora One", sans-serif',
    position: 'relative',
  },
  logoContainer: {
    position: 'absolute', 
    top: '20px', 
    left: '20px',
    display: 'flex', 
    alignItems: 'center',
  },
  title: {
    fontSize: '3rem',
    marginBottom: '20px',
    color: '#FFED89',  // Gold title
    fontFamily: '"Cantora One", sans-serif',
    textShadow: '2px 2px 10px rgba(255, 215, 0, 0.8)',  // Glowing text effect
    animation: 'scaleUp 2s infinite alternate',  // Animate the title with scaling effect
  },
  explanation: {
    fontSize: '1.2rem',
    color: '#FFED89',  // Gold text
    textAlign: 'center',
    maxWidth: '80%',  // Add a max width so it doesn't stretch too far on larger screens
    marginBottom: '30px',  // Adjust the space between explanation and columns
    lineHeight: '1.5',  // Make it more readable
  },
  columns: {
    display: 'flex' as const,
    flexDirection: 'row' as const,
    justifyContent: 'space-between',
    width: '80%',
  },
  leftColumn: {
    flex: 1,
    marginRight: '20px',
  },
  rightColumn: {
    flex: 1,
    marginLeft: '20px',
    maxHeight: '500px',  // Set a maximum height for the question column
    overflowY: 'auto',  // Enable vertical scrolling when content exceeds the height
    paddingRight: '10px',  // Add some padding on the right to avoid overlap with the scrollbar
  },
  subheader: {
    fontSize: '2rem',
    marginBottom: '10px',
    fontFamily: '"Cantora One", sans-serif',
    fontWeight: '400',
    textShadow: '1px 1px 5px rgba(255, 215, 0, 0.8)',
  },
  textarea: {
    width: '100%',
    height: '300px',
    padding: '10px',
    fontSize: '1.2rem',
    borderRadius: '8px',
    border: '2px solid #FFED89',
    backgroundColor: '#1a1a1a',  // Darker background for textarea
    color: '#FFED89',
    resize: 'vertical',
    boxShadow: '0 0 15px rgba(255, 215, 0, 0.5)',  // Gold glow effect
    outline: 'none',  // Remove default outline
    transition: 'box-shadow 0.3s ease',
    ':focus': {
      boxShadow: '0 0 20px rgba(255, 215, 0, 0.8)',  // Stronger glow on focus
    },
  },
  submitButton: {
    padding: '10px 20px',
    fontSize: '1.2rem',
    backgroundColor: '#FFED89',
    color: '#000000',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    marginTop: '10px',
    transition: 'transform 0.2s ease, box-shadow 0.2s ease',
    ':hover': {
      transform: 'scale(1.1)',  // Slight zoom on hover
      boxShadow: '0 0 15px rgba(255, 215, 0, 0.5)',
    },
  },
  questionContainer: {
    width: '100%',
    display: 'flex',
    flexDirection: 'column' as 'column',
  },
  questionBlock: {
    marginBottom: '20px',  // Spacing between each block
    display: 'flex',
    justifyContent: 'center',  // Center the block horizontally
  },
  questionCard: {
    backgroundColor: '#333333',  // Dark gray background
    color: '#FFED89',  // Gold text
    borderRadius: '10px',  // Rounded corners
    padding: '15px',  // Inner padding
    width: '100%',  // Full width of the container
    maxWidth: '600px',  // Limit the max width to prevent too-wide boxes
    boxShadow: '0px 4px 10px rgba(0, 0, 0, 0.5)',  // Add a shadow effect
    border: '1px solid #FFED89',  // Gold border to make it stand out
  },
  questionText: {
    fontSize: '1.2rem',
    marginBottom: '5px',
    color: '#FFED89',  // Gold text for questions
  },
  urlText: {
    fontSize: '0.9rem',
    color: '#FFED89',  // Gold text for URLs
    textDecoration: 'underline',
  },
  error: {
    color: 'red',
  },
};

export default Home;