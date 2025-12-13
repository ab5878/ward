import React, { useState, useRef, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';
import { ArrowLeft, Mic, MicOff, Volume2, Loader2, CheckCircle, AlertTriangle } from 'lucide-react';
import Recorder from 'recorder-js';

export default function VoiceCase() {
  const [step, setStep] = useState(1); // 1-5 for the 5-step protocol
  const [recording, setRecording] = useState(false);
  const [processing, setProcessing] = useState(false);
  
  // Language selection
  const [selectedLanguage, setSelectedLanguage] = useState('hi-IN'); // Default to Hindi
  
  // Step 1: Initial disruption
  const [initialTranscript, setInitialTranscript] = useState('');
  const [detectedLanguage, setDetectedLanguage] = useState('');
  
  // Step 2: Clarity questions
  const [clarityQuestions, setClarityQuestions] = useState([]);
  const [clarityAnswers, setClarityAnswers] = useState({});
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  
  // Step 3: Locked disruption
  const [extractedDisruption, setExtractedDisruption] = useState(null);
  const [disruptionApproved, setDisruptionApproved] = useState(false);
  
  // Step 4: Decision guidance (will redirect to standard flow)
  
  // Conversation transcript
  const [conversationLog, setConversationLog] = useState([]);
  
  // Audio references
  const audioContextRef = useRef(null);
  const recorderRef = useRef(null);
  const audioPlayerRef = useRef(null);
  
  const navigate = useNavigate();

  // Initialize audio context
  useEffect(() => {
    const initAudio = async () => {
      try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        audioContextRef.current = audioContext;
      } catch (error) {
        console.error('Failed to initialize audio context:', error);
      }
    };
    initAudio();
  }, []);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      const recorder = new Recorder(audioContextRef.current, {
        onAnalysed: data => {}
      });
      
      recorder.init(stream);
      await recorder.start();
      
      recorderRef.current = recorder;
      setRecording(true);
    } catch (error) {
      alert('Microphone access denied or not available: ' + error.message);
    }
  };

  const stopRecording = async () => {
    if (!recorderRef.current) return;
    
    setRecording(false);
    const { blob } = await recorderRef.current.stop();
    
    // Convert blob to base64
    const reader = new FileReader();
    reader.onloadend = async () => {
      const base64Audio = reader.result.split(',')[1];
      await processVoiceInput(base64Audio);
    };
    reader.readAsDataURL(blob);
  };

  const processVoiceInput = async (audioBase64) => {
    setProcessing(true);
    
    try {
      // Step 1: Transcribe voice with explicit language code
      const transcribeResponse = await api.post('/voice/transcribe', {
        audio_base64: audioBase64,
        audio_format: 'wav',
        language_code: selectedLanguage  // REQUIRED for Sarvam AI
      });
      
      const transcript = transcribeResponse.data.transcript;
      const languageCode = transcribeResponse.data.language_code;
      
      // Check if transcript is empty
      if (!transcript || transcript.trim().length === 0) {
        alert('No speech detected. Please try speaking again.');
        setProcessing(false);
        return;
      }
      
      // Add to conversation log
      addToConversation('operator', transcript);
      
      if (step === 1) {
        // Initial disruption capture
        setInitialTranscript(transcript);
        setDetectedLanguage(languageCode);
        
        // Generate clarity questions
        const questionsResponse = await api.post('/voice/clarity-questions', {
          transcript: transcript
        });
        
        setClarityQuestions(questionsResponse.data.questions);
        
        // Speak first question
        await speakText(questionsResponse.data.questions[0]);
        
        setStep(2);
        setCurrentQuestionIndex(0);
      } else if (step === 2) {
        // Answering clarity questions
        const newAnswers = { ...clarityAnswers };
        newAnswers[currentQuestionIndex] = transcript;
        setClarityAnswers(newAnswers);
        
        if (currentQuestionIndex < clarityQuestions.length - 1) {
          // Ask next question
          const nextIndex = currentQuestionIndex + 1;
          setCurrentQuestionIndex(nextIndex);
          await speakText(clarityQuestions[nextIndex]);
        } else {
          // All questions answered - extract disruption
          await extractDisruptionDetails();
        }
      }
    } catch (error) {
      console.error('Voice processing error:', error);
      alert('Voice processing failed: ' + (error.response?.data?.detail || error.message));
    } finally {
      setProcessing(false);
    }
  };

  const extractDisruptionDetails = async () => {
    setProcessing(true);
    
    try {
      // Build conversation transcript
      const conversationTranscript = conversationLog
        .map(msg => `${msg.speaker === 'operator' ? 'Operator' : 'Ward'}: ${msg.text}`)
        .join('\n');
      
      // Extract structured disruption
      const extractResponse = await api.post('/voice/extract-disruption', {
        conversation_transcript: conversationTranscript
      });
      
      setExtractedDisruption(extractResponse.data);
      
      // Speak confirmation
      const confirmText = "I've structured your disruption. Please review and approve the details on screen.";
      await speakText(confirmText);
      
      setStep(3);
    } catch (error) {
      console.error('Extraction error:', error);
      alert('Failed to extract disruption: ' + (error.response?.data?.detail || error.message));
    } finally {
      setProcessing(false);
    }
  };

  const speakText = async (text) => {
    try {
      addToConversation('ward', text);
      
      const ttsResponse = await api.post('/voice/text-to-speech', {
        response_text: text,
        context: 'clarity'
      });
      
      // Play audio
      const audio = new Audio(`data:audio/wav;base64,${ttsResponse.data.audio_base64}`);
      audioPlayerRef.current = audio;
      audio.play();
    } catch (error) {
      console.error('TTS error:', error);
      // Fallback: just log the text
    }
  };

  const addToConversation = (speaker, text) => {
    setConversationLog(prev => [
      ...prev,
      {
        speaker,
        text,
        timestamp: new Date().toISOString()
      }
    ]);
  };

  const approveDisruption = async () => {
    setDisruptionApproved(true);
    setProcessing(true);
    
    try {
      // Create case from voice
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
      
      // Navigate to case detail page
      navigate(`/cases/${caseResponse.data._id}`);
    } catch (error) {
      console.error('Case creation error:', error);
      alert('Failed to create case: ' + (error.response?.data?.detail || error.message));
    } finally {
      setProcessing(false);
    }
  };

  const editManually = () => {
    // Redirect to standard form with pre-filled data
    navigate('/cases/new', { 
      state: { 
        prefill: extractedDisruption 
      } 
    });
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-[hsl(var(--border))] bg-card">
        <div className="container mx-auto px-6 py-4">
          <Link
            to="/dashboard"
            className="inline-flex items-center gap-2 text-sm text-[hsl(var(--muted-foreground))] hover:text-foreground transition-colors mb-2"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Dashboard
          </Link>
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold">Voice-First Disruption</h1>
              <p className="text-sm text-[hsl(var(--muted-foreground))]">
                Speak naturally in any Indian language. Ward will guide you.
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs px-3 py-1 bg-[hsl(var(--primary))]/10 text-[hsl(var(--primary))] rounded-full font-medium">
                Powered by Sarvam AI
              </span>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8 max-w-4xl">
        {/* Progress Steps */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            {[1, 2, 3, 4, 5].map((s) => (
              <div
                key={s}
                className={`flex-1 ${s < 5 ? 'mr-2' : ''}`}
              >
                <div
                  className={`h-2 rounded-full ${
                    s <= step
                      ? 'bg-[hsl(var(--primary))]'
                      : 'bg-[hsl(var(--muted))]'
                  }`}
                />
              </div>
            ))}
          </div>
          <div className="flex justify-between text-xs text-[hsl(var(--muted-foreground))]">
            <span>Speak</span>
            <span>Clarify</span>
            <span>Lock</span>
            <span>Guide</span>
            <span>Done</span>
          </div>
        </div>

        {/* Step 1: Initial Disruption */}
        {step === 1 && (
          <div className="bg-card border border-[hsl(var(--border))] rounded-lg p-8 text-center">
            <Mic className="h-16 w-16 mx-auto mb-4 text-[hsl(var(--primary))]" />
            <h2 className="text-2xl font-bold mb-2">Speak the Disruption</h2>
            <p className="text-[hsl(var(--muted-foreground))] mb-6">
              Select your language and describe what just happened.
            </p>
            
            {/* Language Selector */}
            <div className="mb-6 max-w-xs mx-auto">
              <label htmlFor="language" className="block text-sm font-medium mb-2 text-left">
                Select Language *
              </label>
              <select
                id="language"
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className="w-full px-3 py-2 border border-[hsl(var(--input))] rounded-md focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))] bg-background text-left"
                data-testid="language-select"
              >
                <option value="hi-IN">🇮🇳 Hindi (हिन्दी)</option>
                <option value="en-IN">🇮🇳 English (Indian)</option>
                <option value="ta-IN">🇮🇳 Tamil (தமிழ்)</option>
                <option value="te-IN">🇮🇳 Telugu (తెలుగు)</option>
                <option value="kn-IN">🇮🇳 Kannada (ಕನ್ನಡ)</option>
                <option value="ml-IN">🇮🇳 Malayalam (മലയാളം)</option>
                <option value="mr-IN">🇮🇳 Marathi (मराठी)</option>
                <option value="gu-IN">🇮🇳 Gujarati (ગુજરાતી)</option>
                <option value="pa-IN">🇮🇳 Punjabi (ਪੰਜਾਬੀ)</option>
                <option value="bn-IN">🇮🇳 Bengali (বাংলা)</option>
                <option value="od-IN">🇮🇳 Odia (ଓଡ଼ିଆ)</option>
              </select>
            </div>
            
            <p className="text-sm text-[hsl(var(--muted-foreground))] mb-6 italic">
              Example: "Ward, container XYZ is stuck at Mundra. CHA says assessment pending, exact reason not clear yet."
            </p>
            
            {!recording && !processing && (
              <button
                onClick={startRecording}
                className="inline-flex items-center gap-2 px-8 py-4 bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] rounded-md hover:bg-[hsl(var(--primary))]/90 transition-colors text-lg font-medium"
                data-testid="start-recording-button"
              >
                <Mic className="h-5 w-5" />
                Start Speaking
              </button>
            )}
            
            {recording && (
              <div>
                <div className="inline-flex items-center gap-3 mb-4">
                  <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse" />
                  <span className="text-lg font-medium">Recording...</span>
                </div>
                <br />
                <button
                  onClick={stopRecording}
                  className="inline-flex items-center gap-2 px-8 py-4 bg-[hsl(var(--destructive))] text-[hsl(var(--destructive-foreground))] rounded-md hover:bg-[hsl(var(--destructive))]/90 transition-colors"
                  data-testid="stop-recording-button"
                >
                  <MicOff className="h-5 w-5" />
                  Stop & Process
                </button>
              </div>
            )}
            
            {processing && (
              <div className="inline-flex items-center gap-2 text-[hsl(var(--primary))]">
                <Loader2 className="h-5 w-5 animate-spin" />
                <span>Processing with Sarvam AI...</span>
              </div>
            )}
          </div>
        )}

        {/* Step 2: Clarity Questions */}
        {step === 2 && (
          <div className="space-y-6">
            <div className="bg-[hsl(var(--info))]/10 border border-[hsl(var(--info))]/20 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-2">Ward Clarifies — It Does Not Decide</h3>
              <p className="text-sm text-[hsl(var(--muted-foreground))]">
                Answer a few questions to help structure the disruption.
              </p>
            </div>

            <div className="bg-card border border-[hsl(var(--border))] rounded-lg p-6">
              <div className="mb-4">
                <span className="text-xs text-[hsl(var(--muted-foreground))]">
                  Question {currentQuestionIndex + 1} of {clarityQuestions.length}
                </span>
              </div>
              
              <div className="mb-6">
                <div className="flex items-start gap-3 mb-4">
                  <Volume2 className="h-5 w-5 text-[hsl(var(--primary))] mt-1 flex-shrink-0" />
                  <p className="text-lg font-medium">
                    {clarityQuestions[currentQuestionIndex]}
                  </p>
                </div>
              </div>

              {!recording && !processing && (
                <button
                  onClick={startRecording}
                  className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] rounded-md hover:bg-[hsl(var(--primary))]/90 transition-colors"
                >
                  <Mic className="h-5 w-5" />
                  Answer
                </button>
              )}
              
              {recording && (
                <div className="text-center">
                  <div className="inline-flex items-center gap-3 mb-4">
                    <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse" />
                    <span className="font-medium">Recording your answer...</span>
                  </div>
                  <br />
                  <button
                    onClick={stopRecording}
                    className="inline-flex items-center gap-2 px-6 py-3 bg-[hsl(var(--destructive))] text-[hsl(var(--destructive-foreground))] rounded-md"
                  >
                    <MicOff className="h-5 w-5" />
                    Stop
                  </button>
                </div>
              )}
              
              {processing && (
                <div className="text-center text-[hsl(var(--primary))]">
                  <Loader2 className="h-6 w-6 animate-spin mx-auto" />
                </div>
              )}
            </div>

            {/* Already answered */}
            {Object.keys(clarityAnswers).length > 0 && (
              <div className="space-y-2">
                <h4 className="text-sm font-medium text-[hsl(var(--muted-foreground))]">
                  Your Answers:
                </h4>
                {Object.entries(clarityAnswers).map(([index, answer]) => (
                  <div key={index} className="text-sm p-3 bg-[hsl(var(--muted))]/30 rounded">
                    <span className="font-medium">Q{parseInt(index) + 1}:</span> {answer}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Step 3: Locked Disruption */}
        {step === 3 && extractedDisruption && (
          <div className="space-y-6">
            <div className="bg-[hsl(var(--warning))]/10 border border-[hsl(var(--warning))]/20 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-2">Disruption Locked (Human Approval Required)</h3>
              <p className="text-sm text-[hsl(var(--muted-foreground))]">
                Review the extracted details. Approve to proceed or edit manually.
              </p>
            </div>

            <div className="bg-card border border-[hsl(var(--border))] rounded-lg p-6 space-y-4">
              <div>
                <span className="text-sm font-medium text-[hsl(var(--muted-foreground))]">Type:</span>
                <p className="font-medium capitalize">{extractedDisruption.disruption_type?.replace(/_/g, ' ')}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-[hsl(var(--muted-foreground))]">Scope:</span>
                <p>{extractedDisruption.scope}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-[hsl(var(--muted-foreground))]">Identifier:</span>
                <p className="font-mono">{extractedDisruption.identifier}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-[hsl(var(--muted-foreground))]">Time Discovered (IST):</span>
                <p>{extractedDisruption.time_discovered_ist}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-[hsl(var(--muted-foreground))]">Source:</span>
                <p>{extractedDisruption.source}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-[hsl(var(--muted-foreground))]">Description:</span>
                <p className="text-sm">{extractedDisruption.full_description}</p>
              </div>
              {extractedDisruption.explicit_unknowns?.length > 0 && (
                <div>
                  <span className="text-sm font-medium text-[hsl(var(--muted-foreground))]">Explicit Unknowns:</span>
                  <ul className="list-disc list-inside text-sm">
                    {extractedDisruption.explicit_unknowns.map((unknown, idx) => (
                      <li key={idx}>{unknown}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            <div className="flex gap-3">
              <button
                onClick={editManually}
                className="flex-1 px-6 py-3 border border-[hsl(var(--border))] rounded-md hover:bg-[hsl(var(--secondary))] transition-colors"
              >
                Edit Manually
              </button>
              <button
                onClick={approveDisruption}
                disabled={processing}
                className="flex-1 px-6 py-3 bg-[hsl(var(--success))] text-[hsl(var(--success-foreground))] rounded-md hover:bg-[hsl(var(--success))]/90 transition-colors disabled:opacity-50 font-medium"
                data-testid="approve-disruption-button"
              >
                {processing ? (
                  <span className="flex items-center justify-center gap-2">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Creating Case...
                  </span>
                ) : (
                  <span className="flex items-center justify-center gap-2">
                    <CheckCircle className="h-4 w-4" />
                    Approve & Continue
                  </span>
                )}
              </button>
            </div>
          </div>
        )}

        {/* Conversation Log */}
        {conversationLog.length > 0 && (
          <div className="mt-8 bg-card border border-[hsl(var(--border))] rounded-lg p-6">
            <h3 className="text-sm font-medium mb-4 text-[hsl(var(--muted-foreground))]">Conversation Transcript</h3>
            <div className="space-y-2 max-h-60 overflow-y-auto">
              {conversationLog.map((msg, idx) => (
                <div
                  key={idx}
                  className={`text-sm p-3 rounded ${
                    msg.speaker === 'operator'
                      ? 'bg-[hsl(var(--primary))]/10 ml-8'
                      : 'bg-[hsl(var(--muted))]/30 mr-8'
                  }`}
                >
                  <span className="font-medium">
                    {msg.speaker === 'operator' ? 'You' : 'Ward'}:
                  </span>{' '}
                  {msg.text}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
