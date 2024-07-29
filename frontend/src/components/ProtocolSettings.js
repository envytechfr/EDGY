import React, { useState } from 'react';
import axios from 'axios';

function ProtocolSettings() {
  const [protocol, setProtocol] = useState('modbus');
  const [config, setConfig] = useState({});

  const handleSave = () => {
    axios.post('/api/configure', { protocol, config })
      .then(() => {
        alert('Protocol configuration saved');
      })
      .catch(() => {
        alert('Failed to save protocol configuration');
      });
  };

  return (
    <div>
      <h2>Protocol Settings</h2>
      <div>
        <label>Protocol:</label>
        <select value={protocol} onChange={(e) => setProtocol(e.target.value)}>
          <option value="modbus">Modbus</option>
          <option value="mqtt">MQTT</option>
          <option value="snmp">SNMP</option>
          <option value="bacnet">BACnet</option>
        </select>
      </div>
      <div>
        <label>Configuration:</label>
        <textarea value={JSON.stringify(config)} onChange={(e) => setConfig(JSON.parse(e.target.value))} />
      </div>
      <button onClick={handleSave}>Save</button>
    </div>
  );
}

export default ProtocolSettings;
