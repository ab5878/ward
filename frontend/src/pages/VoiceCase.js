import React, { useState, useRef, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';
import { ArrowLeft, Mic, MicOff, Volume2, Loader2, CheckCircle, PlayCircle } from 'lucide-react';
import Recorder from 'recorder-js';
import { Button } from "@/components/ui/button";
import VoiceRecorder from '../components/VoiceRecorder';

export default function VoiceCase({ mode }) {
  const [step, setStep] = useState(1); // 1-5 for the 5-step protocol
  const [recording, setRecording] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('hi-IN');
  const [initialTranscript, setInitialTranscript] = useState('');
  const [detectedLanguage, setDetectedLanguage] = useState('');
  const [clarityQuestions, setClarityQuestions] = useState([]);
  const [clarityAnswers, setClarityAnswers] = useState({});
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [extractedDisruption, setExtractedDisruption] = useState(null);
  const [conversationLog, setConversationLog] = useState([]);
  const [micError, setMicError] = useState(null);
  
  const audioContextRef = useRef(null);
  const recorderRef = useRef(null);
  const audioPlayerRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    // If "Manual Entry" mode was selected (mode="text"), 
    // we could skip to a form, but for now we reuse this flow or redirect.
    // The previous implementation had a logic for prefill.
    if (mode === 'text') {
        // Redirect to a hypothetical manual entry or just let them use voice for now 
        // as "VoiceCase" implies voice. 
        // Actually, let's keep it voice-first but allow "Simulate" which is text-like.
    }

    const initAudio = async () => {
      try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (AudioContext) {
            audioContextRef.current = new AudioContext();
        }
      } catch (error) {
        console.error('Failed to initialize audio context:', error);
      }
    };
    initAudio();
  }, [mode]);

  const startRecording = async () => {
    setMicError(null);
    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error("Browser does not support audio recording");
      }
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new Recorder(audioContextRef.current, { onAnalysed: data => {} });
      recorder.init(stream);
      await recorder.start();
      recorderRef.current = recorder;
      setRecording(true);
    } catch (error) {
      console.error('Microphone error:', error);
      setMicError(error.message || "Microphone access denied");
    }
  };

  const stopRecording = async () => {
    if (!recorderRef.current) return;
    setRecording(false);
    try {
        const { blob } = await recorderRef.current.stop();
        const reader = new FileReader();
        reader.onloadend = async () => {
            const base64Audio = reader.result.split(',')[1];
            await processVoiceInput(base64Audio);
        };
        reader.readAsDataURL(blob);
    } catch(e) {
        console.error(e);
    }
  };

  // --- DEMO SIMULATION ---
  const simulateVoiceInput = async () => {
      // Simulate a realistic driver report in Hindi/English mix
      const mockTranscript = "Hello Ward, container number MSKU123456 is stuck at JNPT gate. Customs officer says documents mismatch. Please help.";
      processTranscript(mockTranscript, "en-IN");
  };

  const processVoiceInput = async (audioBase64) => {
    setProcessing(true);
    try {
      const transcribeResponse = await api.post('/voice/transcribe', {
        audio_base64: audioBase64,
        audio_format: 'wav',
        language_code: selectedLanguage
      });
      const transcript = transcribeResponse.data.transcript;
      const lang = transcribeResponse.data.language_code;
      await processTranscript(transcript, lang);
    } catch (error) {
      console.error('Voice processing error:', error);
      alert('Voice processing failed: ' + (error.response?.data?.detail || error.message));
      setProcessing(false);
    }
  };

  const processTranscript = async (transcript, languageCode) => {
      if (!transcript || transcript.trim().length === 0) {
        alert('No speech detected.');
        setProcessing(false);
        return;
      }
      
      addToConversation('operator', transcript);
      
      if (step === 1) {
        setInitialTranscript(transcript);
        setDetectedLanguage(languageCode);
        
        // Generate clarity questions
        try {
            const questionsResponse = await api.post('/voice/clarity-questions', { transcript });
            setClarityQuestions(questionsResponse.data.questions);
            
            // Speak first question (if audio works), else just log
            await speakText(questionsResponse.data.questions[0]);
            
            setStep(2);
            setCurrentQuestionIndex(0);
        } catch (e) {
            console.error(e);
        }
      } else if (step === 2) {
        const newAnswers = { ...clarityAnswers };
        newAnswers[currentQuestionIndex] = transcript;
        setClarityAnswers(newAnswers);
        
        if (currentQuestionIndex < clarityQuestions.length - 1) {
          const nextIndex = currentQuestionIndex + 1;
          setCurrentQuestionIndex(nextIndex);
          await speakText(clarityQuestions[nextIndex]);
        } else {
          await extractDisruptionDetails();
        }
      }
      setProcessing(false);
  };

  const extractDisruptionDetails = async () => {
    setProcessing(true);
    try {
      const conversationTranscript = conversationLog
        .map(msg => `${msg.speaker === 'operator' ? 'Operator' : 'Ward'}: ${msg.text}`)
        .join('\n');
      
      const extractResponse = await api.post('/voice/extract-disruption', {
        conversation_transcript: conversationTranscript
      });
      setExtractedDisruption(extractResponse.data);
      await speakText("I've structured your disruption. Please review and approve the details.");
      setStep(3);
    } catch (error) {
      console.error(error);
    } finally {
      setProcessing(false);
    }
  };

  const speakText = async (text) => {
    addToConversation('ward', text);
    try {
      const languageForTTS = detectedLanguage || selectedLanguage;
      const ttsResponse = await api.post('/voice/text-to-speech', {
        response_text: text,
        language_code: languageForTTS,
        context: 'clarity'
      });
      const audio = new Audio(`data:audio/wav;base64,${ttsResponse.data.audio_base64}`);
      audioPlayerRef.current = audio;
      await audio.play();
    } catch (error) {
      console.error('TTS error (likely browser block or backend):', error);
    }
  };

  const addToConversation = (speaker, text) => {
    setConversationLog(prev => [
      ...prev,
      { speaker, text, timestamp: new Date().toISOString() }
    ]);
  };

  const approveDisruption = async () => {
    setProcessing(true);
    try {
      const fullTranscript = conversationLog
        .map(msg => `[${msg.timestamp}] ${msg.speaker === 'operator' ? 'Operator' : 'Ward'}: ${msg.text}`)
        .join('\n');
      
      const caseResponse = await api.post('/cases/voice-create', {
        description: extractedDisruption.full_description,
        disruption_details: {
          disruption_type: extractedDisruption.disruption_type,
          scope: extractedDisruption.scope,
          identifier: extractedDisruption.identifier,
          time_discovered_ist: extractedDisruption.time_discovered_ist,
          source: extractedDisruption.source
        },
        shipment_identifiers: {
          ids: [extractedDisruption.identifier],
          routes: [],
          carriers: []
        },
        voice_transcript: fullTranscript
      });
      navigate(`/cases/${caseResponse.data._id}`);
    } catch (error) {
      console.error(error);
      alert('Failed to create case');
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-[hsl(var(--border))] bg-card">
        <div className="container mx-auto px-6 py-4">
          <Link to="/dashboard" className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-900 mb-2">
            <ArrowLeft className="h-4 w-4" /> Back to Dashboard
          </Link>
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold">Voice-First Disruption</h1>
            <span className="text-xs px-3 py-1 bg-blue-100 text-blue-700 rounded-full font-medium">Powered by Sarvam AI</span>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8 max-w-4xl">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            {[1, 2, 3].map((s) => (
              <div key={s} className={`flex-1 h-2 rounded-full mx-1 ${s <= step ? 'bg-blue-600' : 'bg-gray-200'}`} />
            ))}
          </div>
          <div className="flex justify-between text-xs text-gray-500 px-1">
            <span>Report</span>
            <span>Clarify</span>
            <span>Review</span>
          </div>
        </div>

        {step === 1 && (
          <div className="bg-card border rounded-lg p-8 text-center shadow-sm">
            <Mic className="h-16 w-16 mx-auto mb-4 text-blue-600" />
            <h2 className="text-2xl font-bold mb-2">Speak the Disruption</h2>
            <p className="text-gray-500 mb-6">Select your language and describe the issue.</p>
            
            <select
              value={selectedLanguage}
              onChange={(e) => setSelectedLanguage(e.target.value)}
              className="mb-6 px-4 py-2 border rounded-md"
            >
              <option value="hi-IN">🇮🇳 Hindi (हिन्दी)</option>
              <option value="en-IN">🇮🇳 English (Indian)</option>
              {/* Add others as needed */}
            </select>
            
            <div className="flex flex-col gap-4 items-center">
                {/* Use VoiceRecorder component for better UX */}
                <VoiceRecorder
                    onRecordingComplete={async (audioData) => {
                        await processVoiceInput(audioData.audio_base64);
                    }}
                    language={selectedLanguage}
                />
                
                {/* Fallback: Original recording buttons */}
                {!recording && !processing && (
                <button
                    onClick={startRecording}
                    className="flex items-center gap-2 px-8 py-4 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-all text-lg shadow-lg"
                >
                    <Mic className="h-5 w-5" /> Start Speaking (Legacy)
                </button>
                )}
                
                {recording && (
                <button
                    onClick={stopRecording}
                    className="flex items-center gap-2 px-8 py-4 bg-red-500 text-white rounded-full hover:bg-red-600 transition-all text-lg animate-pulse"
                >
                    <MicOff className="h-5 w-5" /> Stop & Process
                </button>
                )}

                {/* DEMO BUTTON FOR BROKEN ENVIRONMENTS */}
                <Button variant="ghost" onClick={simulateVoiceInput} disabled={processing} className="text-xs text-gray-400 hover:text-blue-600">
                    <PlayCircle className="h-3 w-3 mr-1" /> Simulate Demo Input (No Mic)
                </Button>
            </div>

            {micError && <p className="text-red-500 mt-4 text-sm bg-red-50 p-2 rounded">{micError}</p>}
            
            {processing && (
              <div className="mt-6 flex items-center justify-center gap-2 text-blue-600">
                <Loader2 className="h-5 w-5 animate-spin" /> Processing...
              </div>
            )}
          </div>
        )}

        {step === 2 && (
          <div className="bg-card border rounded-lg p-6">
            <div className="flex items-start gap-4 mb-6">
                <div className="p-3 bg-blue-50 rounded-full">
                    <Volume2 className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                    <h3 className="text-lg font-bold text-gray-900">Ward needs clarification</h3>
                    <p className="text-xl mt-2 text-gray-700">{clarityQuestions[currentQuestionIndex]}</p>
                </div>
            </div>
            
            <div className="flex gap-3 justify-center">
                <Button onClick={startRecording} disabled={recording || processing} className="w-full h-12 text-lg">
                    {recording ? "Recording..." : "Answer Voice"}
                </Button>
                {/* Simulation for Step 2 */}
                <Button variant="outline" onClick={() => processTranscript("It is due to a documentation error.", "en-IN")} className="h-12">
                    Simulate Answer
                </Button>
            </div>
          </div>
        )}

        {step === 3 && extractedDisruption && (
          <div className="bg-card border rounded-lg p-6 space-y-6">
            <div className="flex items-center gap-3 text-green-600 bg-green-50 p-4 rounded-lg">
                <CheckCircle className="h-6 w-6" />
                <span className="font-medium">Disruption Structured Successfully</span>
            </div>
            
            <div className="grid grid-cols-2 gap-4 text-sm border p-4 rounded bg-gray-50">
                <div><span className="font-bold block text-gray-500">Type</span> {extractedDisruption.disruption_type}</div>
                <div><span className="font-bold block text-gray-500">Location</span> {extractedDisruption.identifier}</div>
                <div className="col-span-2"><span className="font-bold block text-gray-500">Summary</span> {extractedDisruption.full_description}</div>
            </div>

            <Button onClick={approveDisruption} disabled={processing} className="w-full h-12 text-lg bg-green-600 hover:bg-green-700">
                {processing ? <Loader2 className="animate-spin" /> : "Approve & Create Case"}
            </Button>
          </div>
        )}

        {/* Transcript */}
        {conversationLog.length > 0 && (
            <div className="mt-8 border-t pt-6">
                <h4 className="text-xs font-bold text-gray-400 uppercase mb-4">Transcript</h4>
                <div className="space-y-3">
                    {conversationLog.map((msg, i) => (
                        <div key={i} className={`flex ${msg.speaker === 'operator' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`max-w-[80%] p-3 rounded-lg text-sm ${msg.speaker === 'operator' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-800'}`}>
                                {msg.text}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        )}
      </div>
    </div>
  );
}
