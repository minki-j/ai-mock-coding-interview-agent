import { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { Button } from "@chatscope/chat-ui-kit-react";

const VoiceInput = ({ onTranscriptionComplete, onStart, onStop, isRecording }) => {
  const recognitionRef = useRef(null);

  // Initialize recognition instance once
  useEffect(() => {
    if (!('webkitSpeechRecognition' in window)) {
      console.error('Speech recognition is not supported in this browser');
      return;
    }

    recognitionRef.current = new window.webkitSpeechRecognition();
    const recognition = recognitionRef.current;
    
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
      console.log('Speech recognition started');
      onStart?.();
    };

    recognition.onresult = (event) => {
      let interimTranscript = '';
      let finalTranscript = '';

      for (let i = 0; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript + ' ';
        } else {
          interimTranscript += transcript;
        }
      }

      if (finalTranscript) {
        onTranscriptionComplete(finalTranscript.trim(), true);
      }
      if (interimTranscript) {
        onTranscriptionComplete(interimTranscript.trim(), false);
      }
    };

    recognition.onend = () => {
      console.log('Speech recognition ended');
      // Only restart if we're still supposed to be listening
      if (isRecording) {
        console.log('Restarting recognition');
        try {
          recognition.start();
        } catch (error) {
          console.error('Error restarting recognition:', error);
        }
      }
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
    };

    // Cleanup on component unmount
    return () => {
      recognition.abort();
    };
  }, []); // Empty dependency array - only run once on mount

  // Handle isRecording changes
  useEffect(() => {
    if (isRecording) {
      startRecording();
    } else {
      stopRecording();
    }
  }, [isRecording]);

  const startRecording = () => {
    if (!recognitionRef.current) {
      console.error('Speech recognition not initialized');
      return;
    }

    try {
      recognitionRef.current.start();
    } catch (error) {
      console.error('Error starting recognition:', error);
    }
  };

  const stopRecording = () => {
    if (!recognitionRef.current) {
      console.error('Speech recognition not initialized');
      return;
    }

    try {
      recognitionRef.current.stop();
    } catch (error) {
      console.error('Error stopping recognition:', error);
    }
  };

  if (!('webkitSpeechRecognition' in window)) {
    return null;
  }

  return (
    <div className="flex items-center gap-2 p-2">
      <Button
        onClick={startRecording}
        className={`p-2 rounded-full transition-colors ${
          isRecording
            ? 'bg-red-500 text-white hover:bg-red-600'
            : 'bg-blue-500 text-white hover:bg-blue-600'
        }`}
        title={isRecording ? 'Stop Recording' : 'Start Recording'}
      >
        {isRecording ? (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
          </svg>
        ) : (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
          </svg>
        )}
      </Button>
      {isRecording && (
        <span className="text-sm text-gray-500 animate-pulse">
          Recording...
        </span>
      )}
    </div>
  );
};

VoiceInput.propTypes = {
  onTranscriptionComplete: PropTypes.func.isRequired,
  onStart: PropTypes.func,
  onStop: PropTypes.func,
  isRecording: PropTypes.bool
};

export default VoiceInput; 