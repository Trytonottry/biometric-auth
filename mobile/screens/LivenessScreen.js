import React, { useRef } from 'react';
import { View, Text, Button } from 'react-native';
import { RNCamera } from 'react-native-camera';
import axios from '../services/api';

const LivenessScreen = () => {
  const cameraRef = useRef(null);

  const takePicture = async () => {
    if (cameraRef.current) {
      const options = { quality: 0.5, base64: true };
      const data = await cameraRef.current.takePictureAsync(options);

      // Отправляем кадр на сервер для проверки живости
      const res = await axios.post('/api/verify-live', { image: data.base64 });
      if (res.data.live) {
        alert("✅ Проверка пройдена!");
        // Можно отправить push-подтверждение
      }
    }
  };

  return (
    <View style={{ flex: 1 }}>
      <RNCamera
        ref={cameraRef}
        style={{ flex: 1 }}
        type={RNCamera.Constants.Type.front}
      />
      <Button title="Сделать фото" onPress={takePicture} />
    </View>
  );
};

export default LivenessScreen;