import React, { useState } from 'react';
import axios from 'axios';

function Settings() {
  const [connectionType, setConnectionType] = useState('LAN');
  const [ipAddress, setIpAddress] = useState('');
  const [netmask, setNetmask] = useState('');
  const [gateway, setGateway] = useState('');
  const [ssid, setSsid] = useState('');
  const [password, setPassword] = useState('');

  const handleSave = () => {
    const config = {
      connection_type: connectionType,
      ip_address: ipAddress,
      netmask,
      gateway,
      ssid,
      password
    };
    axios.post('/api/configure_network', config)
      .then(() => {
        alert('Network configuration updated');
      })
      .catch(() => {
        alert('Failed to update network configuration');
      });
  };

  return (
    <div>
      <h2>Settings</h2>
      <div>
        <label>Connection Type:</label>
        <select value={connectionType} onChange={(e) => setConnectionType(e.target.value)}>
          <option value="LAN">LAN</option>
          <option value="WiFi">WiFi</option>
        </select>
      </div>
      {connectionType === 'LAN' ? (
        <>
          <div>
            <label>IP Address:</label>
            <input type="text" value={ipAddress} onChange={(e) => setIpAddress(e.target.value)} />
          </div>
          <div>
            <label>Netmask:</label>
            <input type="text" value={netmask} onChange={(e) => setNetmask(e.target.value)} />
          </div>
          <div>
            <label>Gateway:</label>
            <input type="text" value={gateway} onChange={(e) => setGateway(e.target.value)} />
          </div>
        </>
      ) : (
        <>
          <div>
            <label>SSID:</label>
            <input type="text" value={ssid} onChange={(e) => setSsid(e.target.value)} />
          </div>
          <div>
            <label>Password:</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </div>
        </>
      )}
      <button onClick={handleSave}>Save</button>
    </div>
  );
}

export default Settings;
