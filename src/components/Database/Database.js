import React, { useState, useEffect } from 'react';
import { fetchData, sendData, queryLLM } from "../../api";
import './Database.css'; // Import the CSS file
import { TextField, IconButton, Typography, Table, TableBody, TableCell, TableHead, TableRow, Paper, List, ListItem, ListItemText, Divider, InputAdornment } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

const Database = () => {
    const [data, setData] = useState([]); // Data from the database
    const [userInput, setUserInput] = useState(""); // User's input
    const [chatHistory, setChatHistory] = useState([]); // Chat messages

    // Fetch database data on component mount
    useEffect(() => {
        fetchData().then(setData).catch(err => console.error("Failed to fetch data:", err));
    }, []);

    // Handle submit action
    const handleSubmit = async () => {
        if (userInput.trim() === "") return;

        const userMessage = { user: "You", text: userInput }; // Save user message
        setChatHistory((prev) => [...prev, userMessage]); // Add user message to chat history
        setUserInput(""); // Clear input box

        try {
            // Get the LLM response
            const llmResponse = await queryLLM(userInput);

            if (llmResponse.error) {
                const botMessage = { user: "Bot", text: `Error: ${llmResponse.error}` };
                setChatHistory((prev) => [...prev, botMessage]);
                return;
            }

            const { action, key, value } = llmResponse;

            if (!action || !key) {
                const botMessage = { user: "Bot", text: "Invalid data extracted. Action and Key are required." };
                setChatHistory((prev) => [...prev, botMessage]);
                return;
            }

            // Send data to the backend
            const action1 = await sendData({ action, key, value });

            // Refresh the database table
            fetchData().then(setData);

            let botMessageText = "";
            if (action1["message"] === 'update') {
                botMessageText = `Key already exists in database. Key: ${key} and Value: ${value || "N/A"} updated successfully in the database`;
            }
            else if (action === "insert") {
                botMessageText = `Key: ${key} and Value: ${value || "N/A"} inserted successfully in the database`;
            } else if (action === "update") {
                botMessageText = `Key: ${key} and Value: ${value || "N/A"} updated successfully in the database`;
            } else if (action === "delete") {
                botMessageText = `Key: ${key} deleted successfully from the database`;
            } else {
                botMessageText = `Action: ${action} with Key: ${key} performed successfully`;
            }

            const botMessage = { user: "Genie", text: botMessageText };
            setChatHistory((prev) => [...prev, botMessage]);
        } catch (error) {
            console.error("Error handling submission:", error);
            const botMessage = { user: "Bot", text: "An error occurred. Please try again." };
            setChatHistory((prev) => [...prev, botMessage]);
        }
    };

    return (
        <div className="database-container">
            {/* Chat Section */}
            <div className="chat-section">
                <Typography variant="h4" className="chat-header">Chat</Typography>

                {/* Chat History */}
                <Paper className="chat-box">
                    <List>
                        {chatHistory.map((message, index) => (
                            <React.Fragment key={index}>
                                <ListItem className={message.user === "You" ? "user-message" : "bot-message"}>
                                    <ListItemText
                                        primary={`${message.user}:`}
                                        secondary={message.text}
                                        sx={{ textAlign: message.user === "You" ? "right" : "left" }}
                                        className={message.user === "You" ? "user-text" : "bot-text"}
                                    />
                                </ListItem>
                            </React.Fragment>
                        ))}
                    </List>
                </Paper>

                {/* Input Bar */}
                <div className="chat-input">
                    <TextField
                        fullWidth
                        variant="outlined"
                        value={userInput}
                        onChange={(e) => setUserInput(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === "Enter") {
                                handleSubmit(); // Trigger the send button when Enter is pressed
                                e.preventDefault(); // Prevent default Enter behavior
                            }
                        }}
                        placeholder="Enter your instruction (e.g., Insert key 'test' with value '123')"
                        className="input-field"
                        required
                        InputProps={{
                            endAdornment: (
                                <InputAdornment position="end">
                                    <IconButton onClick={handleSubmit} color="primary" size="large" className="send-button">
                                        <SendIcon />
                                    </IconButton>
                                </InputAdornment>
                            ),
                        }}
                    />
                </div>
            </div>

            {/* Database Section */}
            <div className="table-section">
                <Typography variant="h4" className="table-header">Database</Typography>

                {/* Data Table */}
                <Paper className="table-container">
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Key</TableCell>
                                <TableCell>Value</TableCell>
                                <TableCell>Created At</TableCell>
                                <TableCell>Updated At</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {data.map((item, idx) => (
                                <TableRow key={idx}>
                                    <TableCell>{item.key}</TableCell>
                                    <TableCell>{item.value}</TableCell>
                                    <TableCell>{item.created_at}</TableCell>
                                    <TableCell>{item.updated_at || 'N/A'}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </Paper>
            </div>
        </div>
    );
};

export default Database;