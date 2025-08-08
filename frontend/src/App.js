import React, { useState } from 'react';
import './App.css';

function App() {
  const [username, setUsername] = useState('');
  const [methods, setMethods] = useState([]);
  const [message, setMessage] = useState('');

  const handleLogin = async () => {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, methods })
    });
    const data = await res.json();
    setMessage(data.message);
  };

  const handleRegister = async () => {
    const res = await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username,
        role: 'user',
        access_level: 1,
        enable_face: methods.includes('face')
      })
    });
    const data = await res.json();
    setMessage(data.error ? `Ошибка: ${data.error}` : 'Зарегистрирован!');
  };

  return (
    <div className="App">
      <h1>🔐 Биометрическая аутентификация</h1>

      <input
        placeholder="Имя пользователя"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      <div>
        <label><input type="checkbox" value="face"
          onChange={(e) => e.target.checked ? setMethods([...methods, 'face']) : setMethods(methods.filter(m => m !== 'face'))}
        /> Лицо</label>

        <label><input type="checkbox" value="fingerprint"
          onChange={(e) => e.target.checked ? setMethods([...methods, 'fingerprint']) : setMethods(methods.filter(m => m !== 'fingerprint'))}
        /> Отпечаток</label>

        <label><input type="checkbox" value="iris"
          onChange={(e) => e.target.checked ? setMethods([...methods, 'iris']) : setMethods(methods.filter(m => m !== 'iris'))}
        /> Радужка</label>
      </div>

      <button onClick={handleLogin}>Войти</button>
      <button onClick={handleRegister}>Зарегистрироваться</button>

      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default App;