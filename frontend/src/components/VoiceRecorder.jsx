import React, { useState, useRef, useEffect } from 'react';
import { Mic, Square, Play, Pause, Loader2 } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import { toast } from 'sonner';

export default function VoiceRecorder({ onRecordingComplete, language = 'hi-IN' }) {
  const [isRecording, setIsRecording] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioBlob, setAudioBlob] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const timerRef = useRef(null);

  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioUrl]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        setAudioBlob(blob);
        setAudioUrl(URL.createObjectURL(blob));
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
      setIsPaused(false);
      setRecordingTime(0);

      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);

      toast.success('Recording started');
    } catch (error) {
      console.error('Error starting recording:', error);
      toast.error('Failed to start recording. Please check microphone permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setIsPaused(false);
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      toast.success('Recording stopped');
    }
  };

  const pauseRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      if (isPaused) {
        mediaRecorderRef.current.resume();
        setIsPaused(false);
        timerRef.current = setInterval(() => {
          setRecordingTime(prev => prev + 1);
        }, 1000);
      } else {
        mediaRecorderRef.current.pause();
        setIsPaused(true);
        if (timerRef.current) {
          clearInterval(timerRef.current);
        }
      }
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleUpload = async () => {
    if (!audioBlob) return;

    setIsUploading(true);
    try {
      // Convert blob to base64
      const reader = new FileReader();
      reader.onloadend = async () => {
        const base64Audio = reader.result.split(',')[1];
        
        if (onRecordingComplete) {
          await onRecordingComplete({
            audio_base64: base64Audio,
            audio_format: 'webm',
            language_code: language
          });
        }
        
        setIsUploading(false);
        setAudioBlob(null);
        setAudioUrl(null);
        setRecordingTime(0);
      };
      reader.readAsDataURL(audioBlob);
    } catch (error) {
      console.error('Error uploading recording:', error);
      toast.error('Failed to upload recording');
      setIsUploading(false);
    }
  };

  const handleDiscard = () => {
    setAudioBlob(null);
    setAudioUrl(null);
    setRecordingTime(0);
    if (audioUrl) {
      URL.revokeObjectURL(audioUrl);
    }
  };

  return (
    <Card className="w-full">
      <CardContent className="p-6">
        <div className="flex flex-col items-center gap-4">
          {/* Recording Status */}
          {isRecording && (
            <div className="flex items-center gap-2 text-red-600">
              <div className="w-3 h-3 bg-red-600 rounded-full animate-pulse"></div>
              <span className="font-semibold">Recording: {formatTime(recordingTime)}</span>
            </div>
          )}

          {/* Audio Player */}
          {audioUrl && !isRecording && (
            <div className="w-full">
              <audio src={audioUrl} controls className="w-full mb-4" />
              <div className="flex gap-2 justify-center">
                <Button
                  onClick={handleUpload}
                  disabled={isUploading}
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  {isUploading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Uploading...
                    </>
                  ) : (
                    'Upload Recording'
                  )}
                </Button>
                <Button
                  onClick={handleDiscard}
                  variant="outline"
                  disabled={isUploading}
                >
                  Discard
                </Button>
              </div>
            </div>
          )}

          {/* Recording Controls */}
          {!audioUrl && (
            <div className="flex flex-col items-center gap-4">
              {!isRecording ? (
                <Button
                  onClick={startRecording}
                  size="lg"
                  className="bg-red-600 hover:bg-red-700 text-white rounded-full w-20 h-20"
                >
                  <Mic className="h-8 w-8" />
                </Button>
              ) : (
                <div className="flex gap-4">
                  <Button
                    onClick={pauseRecording}
                    size="lg"
                    variant="outline"
                    className="rounded-full w-16 h-16"
                  >
                    {isPaused ? (
                      <Play className="h-6 w-6" />
                    ) : (
                      <Pause className="h-6 w-6" />
                    )}
                  </Button>
                  <Button
                    onClick={stopRecording}
                    size="lg"
                    className="bg-red-600 hover:bg-red-700 text-white rounded-full w-16 h-16"
                  >
                    <Square className="h-6 w-6" />
                  </Button>
                </div>
              )}
              
              <p className="text-sm text-gray-600 text-center">
                {!isRecording
                  ? 'Tap to start recording'
                  : isPaused
                  ? 'Recording paused'
                  : 'Recording in progress...'}
              </p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

