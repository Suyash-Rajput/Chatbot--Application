import { useState } from "react";
import "./App.css";

export default function App() {
  const [result, setResult] = useState("");
  const [question, setQuestion] = useState("");
  const [file_type, setType] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [popupVisible, setPopupVisible] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleQuestionChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuestion(event.target.value);
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      console.log(" -----------", selectedFile.type)
      const allowedTypes = ["text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/pdf", "text/csv"];
      if (allowedTypes.includes(selectedFile.type)) {
        setFile(selectedFile);
        setErrorMessage("");
        setPopupVisible(true);
        setType(selectedFile.type);
      } else {
        setFile(null)
        window.alert("Unsupported file type. Please upload a .txt, .docx, .pdf, or .csv file.");
      }
    }
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    // Clear the result when submitting the form
    setResult("");

    const formData = new FormData();

    if (!file || !question || file == null) {
      window.alert("Please provide both file and question.");
      return;
    }

    formData.append("file", file);
    formData.append("question", question);
    formData.append("fileType", file_type);
    fetch("https://chatbot-application-12.onrender.com/predict", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        // Update the result when response is received
        setResult(data.result);
      })
      .catch((error) => {
        console.error("Error", error);
        setErrorMessage("An error occurred while processing your request. Please try again later.");
      });
  };

  return (
    <div className="App">
      {popupVisible && (
        <div className="popup">
          <p>File uploaded successfully!</p>
          <button onClick={() => setPopupVisible(false)}>Close</button>
        </div>
      )}
      <form onSubmit={handleSubmit} className="form">
        <label className="questionLabel" htmlFor="question">
          Question:
        </label>
        <input
          className="questionInput"
          id="question"
          type="text"
          value={question}
          onChange={handleQuestionChange}
          placeholder="Ask your question here"
        />

        <br />
        <label className="fileLabel" htmlFor="file">
          Upload File (.txt, .docx, .pdf, .csv):
        </label>

        <input
          type="file"
          id="file"
          name="file"
          accept=".txt,.docx,.pdf,.csv"
          onChange={handleFileChange}
          className="fileInput"
        />
        {errorMessage && <p className="error">{errorMessage}</p>}
        <br />
        <button
          className={`submitBtn ${(file && question.trim()) ? '' : 'dull'}`}
          type="submit"
          disabled={!file && !question.trim()}>
          Submit
        </button>
      </form>
      <p className="resultOutput">Result: {result}</p>
    </div>
  );
}
