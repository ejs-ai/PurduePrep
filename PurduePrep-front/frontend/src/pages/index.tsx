import Image from 'next/image';
import { useState, useEffect } from 'react';

interface QuestionData {
  question: string;
  url: string;
}

const Home: React.FC = () => {
  const [inputText, setInputText] = useState<string>('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [filename, setFilename] = useState<string>('');
  const [questions, setQuestions] = useState<QuestionData[]>([]);  // For questions and URLs
  const [error, setError] = useState<string | null>(null);  // For error handling
  const [loading, setLoading] = useState<boolean>(false);
  const [timeoutReached, setTimeoutReached] = useState<boolean>(false); // To control error timeout
  const [numQuestions, setNumQuestions] = useState<number>(15); // Default to 15 questions

  // Handle input via text or file
  const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>): void => {
    setInputText(event.target.value);
    setSelectedFile(null);  // Clear selected file if text input is used
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const file = event.target.files?.[0] || null;
    setSelectedFile(file);
    setFilename(file ? file.name : '');  // Update filename state
    setInputText('');  // Clear text input if file is selected
  };

  const handleNumQuestionsChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const value = Math.min(Math.max(Number(event.target.value), 1), 30); // Restrict max value to 30
    setNumQuestions(value);
  };

  // Send input (text or file) to Flask backend
  const handleSubmit = async () => {
    try {
      console.log('start handle submit');
      let response;
      
      // Check if a file is selected, use FormData for file upload
      if (selectedFile) {
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('numQuestions', numQuestions.toString());
        
        response = await fetch('/api/receive-text', {
          method: 'POST',
          body: formData,
        });
      } else {
        // Otherwise, send text input as JSON
        response = await fetch('/api/receive-text', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            inputText: inputText,
            numQuestions: numQuestions // Add numQuestions to JSON payload
          }),
        });
      }
      
      const data = await response.json();
      console.log(data);

      if (data.message === 'Text received successfully') {
        console.log('Text received successfully');
        fetchQuestions();  // Fetch questions from backend on success
      } else {
        setError('Failed to submit input.');
      }
    } catch (error) {
      console.error('Error sending data to backend:', error);
      setError('Error communicating with backend.');
    }
  };

  // Timeout function
  const setErrorTimeout = () => {
    return setTimeout(() => {
      setTimeoutReached(true); // Flag that we have hit the timeout
      setError('Please be patient. Questions loading!');  // Show error after timeout
    }, 60000);  // Timeout set for 60 seconds
  };

  // Fetch questions from the Flask backend
  const fetchQuestions = async () => {
    setLoading(true);  // Start loading when request starts
    setError(null);  // Clear any previous errors
  
    const errorTimeout = setErrorTimeout(); // Start timeout when fetching questions
  
    try {
      const response = await fetch('https://flask-824914791442.us-central1.run.app/api/get-questions');  // Adjust URL based on your setup, http://127.0.0.1:5000/api/get-questions for local
      const data = await response.json();
      console.log(data.questions);
      
      if (response.ok) {
        console.log('response ok');
        setQuestions(data.questions);  // Set questions from backend
        clearTimeout(errorTimeout);  // Clear the timeout since we got a successful response
        setTimeoutReached(false); // Reset timeout flag
        setError(null); // clear the errors
        setLoading(false);  // End loading state
      } else {
        console.error(`Error: ${response.status}, ${await response.text()}`);
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
    //fetchQuestions();
  }, []);

  return (

    <div className="container">
      <div className="logo-container">
        <Image
          src="/images/ece-logo.jpg"
          alt="ECE Logo"
          width={100}
          height={50}
        />
      </div>
      <h1 className="title">PurduePrep 1.0.0</h1>
      <p className="explanation">
        PurduePrep finds real exam questions from universities to match your text or document input. We recommend inputting course notes!
      </p>
      <div className="columns">
        <div className="left-column">
          <h2 className="subheader">Input (text, .txt, or .pdf):</h2>
          <textarea
            value={inputText}
            onChange={handleInputChange}
            placeholder="Type something here..."
            className="textarea"
            wrap="soft"
          />
          <label htmlFor="file-upload" className="file-upload-button">Choose File</label>
          <input 
            id="file-upload" 
            type="file" 
            onChange={handleFileChange} 
            className="hidden-file-input"
          />
          <span className="filename-display">{filename || 'No file chosen'}</span>
          <div className="num-questions-container">
            <label className="num-questions-label" htmlFor="numQuestions">Number of Questions:</label>
            <input
              type="number"
              id="numQuestions"
              value={numQuestions}
              min="1"
              max="30"
              onChange={handleNumQuestionsChange}
              className="num-questions-input"
            />
          </div>
          <button onClick={handleSubmit} className="submit-button">Submit</button>
        </div>
        
        <div className="right-column">
          <h2 className="subheader">Practice Questions:</h2>
          {loading && <p>Loading questions...</p>}
          {timeoutReached && error && <p className="error">{error}</p>}
          <div className="questionContainer">
            {questions.map((item, index) => (
              <div key={index} className="questionBlock">
                <div className="questionCard">
                  <p>{item.question}</p>
                  <a href={item.url} className="urlText" target="_blank" rel="noopener noreferrer">
                    {item.url}
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;