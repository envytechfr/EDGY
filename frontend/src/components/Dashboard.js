import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Dashboard() {
  const [data, setData] = useState('');

  useEffect(() => {
    axios.get('/api/data')
      .then(response => {
        setData(response.data.data);
      });
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>
      <div>Data: {data}</div>
    </div>
  );
}

export default Dashboard;
