import React, { useState } from 'react';
import ReactFlow, { Background, Controls } from 'react-flow-renderer';
import axios from 'axios';

const initialElements = [
  {
    id: '1',
    type: 'default',
    position: { x: 100, y: 100 },
    data: { label: 'EC2 Instance' }
  },
  {
    id: '2',
    type: 'default',
    position: { x: 300, y: 100 },
    data: { label: 'S3 Bucket' }
  }
];

function App() {
  const [elements, setElements] = useState(initialElements);

  const handleGenerate = async () => {
    const payload = {
      resources: elements.map((el) => ({
        type: el.data.label.includes("EC2") ? "ec2" : "s3",
        name: `resource_${el.id}`,
        properties: {
          instance_type: "t2.micro",
          versioning: el.data.label.includes("S3") ? "true" : "false"
        }
      }))
    };

    const response = await axios.post('http://localhost:8000/generate-terraform/', payload);
    alert(response.data.terraform);
  };

  return (
    <div style={{ height: '100vh' }}>
      <ReactFlow elements={elements} onElementsRemove={setElements}>
        <Background />
        <Controls />
      </ReactFlow>
      <div style={{ position: 'absolute', top: 10, right: 10 }}>
        <button onClick={handleGenerate}>Generate Terraform</button>
      </div>
    </div>
  );
}

export default App;
