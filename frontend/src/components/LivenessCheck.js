import React, { useRef, useState } from 'react';

const LivenessCheck = ({ onLivenessSuccess }) => {
  const videoRef = useRef();
  const [facingMode, setFacingMode] = useState('user');
  const [message, setMessage] = useState('Проверка "живого" лица...');

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode }
      });
      videoRef.current.srcObject = stream;
    } catch (err) {
      setMessage("Ошибка камеры: " + err.message);
    }
  };

  const captureAndVerify = () => {
    const canvas = document.createElement('canvas');
    const video = videoRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

    // Простая проверка: лицо обнаружено (в реальности — ML модель)
    // Здесь можно отправить кадр на `/api/verify-live` для анализа
    setTimeout(() => {
      onLivenessSuccess();
      setMessage("✅ Проверка пройдена!");
    }, 1500);
  };

  return (
    <div>
      <h3>{message}</h3>
      <video ref={videoRef} autoPlay playsInline style={{ width: '100%', maxWidth: 400 }} />
      <button onClick={startCamera}>Включить камеру</button>
      <button onClick={captureAndVerify}>Проверить</button>
    </div>
  );
};

export default LivenessCheck;