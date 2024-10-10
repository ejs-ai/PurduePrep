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

  // Handle input via text or file
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputText(event.target.value);
  };
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
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
    try {
      const response = await fetch('http://127.0.0.1:5328/api/get-questions'); // Adjust URL based on your setup
      const data = await response.json();
      setQuestions(data.questions);  // Set questions from backend
    } catch (error) {
      setError('Failed to load questions.');
      console.error('Error fetching questions:', error);
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
      <div style={styles.columns}>
        {/* Left Column for Input */}
        <div style={styles.leftColumn}>
          <h2 style={styles.subheader}>Input (text, .txt, or .pdf:)</h2>
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
          {error && <p style={styles.error}>{error}</p>}
          <div style={styles.questionContainer}>
          {questions && questions.length > 0 ? (
            questions.map((q, index) => (
              <div key={index} style={styles.questionBlock}>
                <h3 style={styles.questionText}>{q.question}</h3>
                <a href={q.url} target="_blank" rel="noopener noreferrer" style={styles.urlText}>
                  {q.url}
                </a>
              </div>
            ))
          ) : (
            <p>No questions available</p>
          )}
          </div>
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column' as 'column',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    backgroundColor: '#000000',  // Black background
    color: '#FFD700',  // Gold text
    fontFamily: '"Cantora One", sans-serif',
    position: 'relative', // Enable absolute positioning of children
  },
  logoContainer: {
    position: 'absolute', // Position it absolutely
    top: '20px', // Adjust the top position
    left: '20px', // Adjust the left position
    display: 'flex', // Use flex to align images next to each other
    alignItems: 'center', // Center the logos vertically
  },
  title: {
    fontSize: '3rem',
    marginBottom: '20px',
    color: '#FFD700',  // Gold title
    fontFamily: '"Cantora One", sans-serif',
  },
  columns: {
    display: 'flex',
    flexDirection: 'row' as 'row',
    justifyContent: 'space-between',
    width: '80%',  // Adjust the width as needed
  },
  leftColumn: {
    flex: 1,
    marginRight: '20px',
  },
  rightColumn: {
    flex: 1,
    marginLeft: '20px',
  },
  subheader: {
    fontSize: '2rem',
    marginBottom: '10px',
    fontFamily: '"Cantora One", sans-serif',  // Use the custom font for subheaders
    fontWeight: '400',  // Regular font weight for subheaders
  },
  textarea: {
    width: '100%',
    height: '300px',
    padding: '10px',
    fontSize: '1.2rem',
    borderRadius: '8px',
    border: '2px solid #FFD700',  // Gold border
    backgroundColor: '#333333',  // Dark gray background
    color: '#FFD700',  // Gold text
    resize: 'vertical',
  },
  submitButton: {
    padding: '10px 20px',
    fontSize: '1.2rem',
    backgroundColor: '#FFD700',  // Gold button
    color: '#000000',  // Black text
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    marginTop: '10px',
  },
  questionContainer: {
    width: '100%',
  },
  questionBlock: {
    marginBottom: '20px',
  },
  questionText: {
    fontSize: '1.2rem',
    marginBottom: '5px',
    color: '#FFD700',  // Gold text for questions
  },
  urlText: {
    fontSize: '0.9rem',
    color: '#FFD700',  // Gold text for URLs
    textDecoration: 'underline',
  },
  error: {
    color: 'red',
  },
};

export default Home;
