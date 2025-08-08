import React, { useEffect, useState } from 'react';
import Chart from 'chart.js/auto';
import { Line } from 'react-chartjs-2';

const AdminDashboard = () => {
  const [users, setUsers] = useState([]);
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    fetch('/api/users', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    }).then(r => r.json()).then(setUsers);

    fetch('/api/logs', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    }).then(r => r.json()).then(setLogs);
  }, []);

  const chartData = {
    labels: ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
    datasets: [{
      label: 'Успешные входы',
      data: [12, 19, 3, 5, 12, 3, 8],
      borderColor: 'green',
      tension: 0.1
    }]
  };

  return (
    <div>
      <h2>🔐 Админ-панель</h2>
      <h3>Пользователи</h3>
      <ul>
        {users.map(u => <li key={u.id}>{u.username} ({u.role})</li>)}
      </ul>

      <h3>Активность</h3>
      <Line data={chartData} />

      <h3>Журнал событий</h3>
      <ul>
        {logs.map((log, i) => (
          <li key={i} style={{ color: log.anomaly_flag ? 'red' : 'black' }}>
            {log.username} — {log.method} — {log.success ? 'Успех' : 'Ошибка'}
            {log.anomaly_flag && " ⚠️ Аномалия"}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AdminDashboard;