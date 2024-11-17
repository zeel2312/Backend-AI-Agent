import axios from 'axios';

const API_BASE = "http://127.0.0.1:5000";

// Fetch data from the backend
export const fetchData = async () => {
    try {
        const response = await axios.get(`${API_BASE}/api/data`);
        return response.data;
    } catch (error) {
        console.error("Error fetching data:", error);
        throw error;
    }
};

// Send data to the backend
export const sendData = async (data) => {
    try {
        const response = await axios.post(`${API_BASE}/api/data`, data);
        console.log(response.data)
        return response.data;
    } catch (error) {
        console.error("Error sending data:", error);
        throw error;
    }
};

// Query the LLM
export const queryLLM = async (userInput) => {
    try {
        const response = await axios.post(`${API_BASE}/api/query_llm`, { user_input: userInput });
        return response.data;
    } catch (error) {
        console.error("Error querying LLM:", error);
        throw error;
    }
};
