import React, { useState } from 'react';
import FileUpload from '../components/FileUpload';
import ModelTrainButton from '../components/ModelTrainButton';
import XAIGenerationButton from '../components/XAIGenerationButton';
import ResultsDisplay from '../components/ResultsDisplay';
import { uploadFiles, trainModel, generateXAI, getResults } from '../api/backend';

function HomePage() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [loadingTrain, setLoadingTrain] = useState(false);
  const [loadingXAI, setLoadingXAI] = useState(false);
  const [results, setResults] = useState(null);

  const handleFilesSelected = files => setSelectedFiles(files);

  const handleUpload = async () => {
    if (!selectedFiles.length) {
      alert('Please select files first.');
      return;
    }
    try {
      await uploadFiles(selectedFiles);
      alert('Files uploaded successfully!');
    } catch (err) {
      alert('Upload failed: ' + err.message);
    }
  };

  const handleTrain = async () => {
    setLoadingTrain(true);
    try {
      const resp = await trainModel();
      setResults(resp.data);
    } catch (err) {
      setResults({ error: err.message });
    }
    setLoadingTrain(false);
  };

  const handleXAI = async () => {
    setLoadingXAI(true);
    try {
      const resp = await generateXAI();
      setResults(resp.data);
    } catch (err) {
      setResults({ error: err.message });
    }
    setLoadingXAI(false);
  };

  return (
    <div style={{ padding: 40, maxWidth: 600, margin: 'auto' }}>
      <h2>OFIDS System Prototype</h2>
      <FileUpload onFilesSelected={handleFilesSelected} />
      <button onClick={handleUpload} style={{ marginRight: 10, marginTop: 10 }}>
        Upload Files
      </button>
      <ModelTrainButton onClick={handleTrain} loading={loadingTrain} />
      <XAIGenerationButton onClick={handleXAI} loading={loadingXAI} />
      <ResultsDisplay results={results} />
    </div>
  );
}

export default HomePage;
