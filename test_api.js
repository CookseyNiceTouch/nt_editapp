const axios = require('axios');

async function testAPI() {
  const baseURL = 'http://localhost:4000';
  
  console.log('Testing Orchestrator API with unique port configuration...\n');
  
  try {
    // Test health endpoint
    console.log('1. Testing health endpoint...');
    const health = await axios.get(`${baseURL}/health`);
    console.log('✅ Health:', health.data);
    
    // Test transcription service health
    console.log('\n2. Testing transcription service health...');
    const transcribeHealth = await axios.get(`${baseURL}/api/transcribe/health`);
    console.log('✅ Transcription Health:', transcribeHealth.data);
    
    // Test queue status
    console.log('\n3. Testing queue status...');
    const queueStatus = await axios.get(`${baseURL}/api/transcribe/queue`);
    console.log('✅ Queue Status:', queueStatus.data);
    
    // Test analyzed files
    console.log('\n4. Testing analyzed files...');
    const analyzedFiles = await axios.get(`${baseURL}/api/transcribe/analyzed`);
    console.log('✅ Analyzed Files:', analyzedFiles.data);
    
    // Test direct Python API on new port
    console.log('\n5. Testing direct Python API (port 8001)...');
    try {
      const directAPI = await axios.get('http://127.0.0.1:8001/');
      console.log('✅ Direct Python API:', directAPI.data);
    } catch (error) {
      console.log('⚠️  Direct Python API not ready:', error.response?.status || error.message);
    }
    
  } catch (error) {
    console.error('❌ Error:', error.response?.data || error.message);
    if (error.response?.status) {
      console.error('Status:', error.response.status);
    }
  }
}

testAPI(); 