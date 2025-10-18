class PropertyChat {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.userInput = document.getElementById('userInput');
        this.sendButton = document.getElementById('sendButton');
        this.apiBase = 'http://localhost:8000/api';
        
        this.initializeEventListeners();
    }
    
    initializeEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }
    
    async sendMessage() {
        const message = this.userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        this.addMessage(message, 'user');
        this.userInput.value = '';
        this.setLoading(true);
        
        try {
            const response = await this.sendToBackend(message);
            this.addBotResponse(response);
        } catch (error) {
            this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            console.error('Error:', error);
        } finally {
            this.setLoading(false);
        }
    }
    
    async sendToBackend(message) {
        const response = await fetch(`${this.apiBase}/chat/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: message })
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        return await response.json();
    }
    
    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        if (typeof content === 'string') {
            contentDiv.textContent = content;
        } else {
            // Handle structured response
            this.formatStructuredResponse(contentDiv, content);
        }
        
        messageDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    formatStructuredResponse(container, response) {
        // Add summary
        const summaryDiv = document.createElement('div');
        summaryDiv.textContent = response.summary;
        summaryDiv.style.marginBottom = '15px';
        container.appendChild(summaryDiv);
        
        // Add property cards if available
        if (response.properties && response.properties.length > 0) {
            const cardsContainer = document.createElement('div');
            cardsContainer.className = 'property-cards';
            
            response.properties.forEach(property => {
                const card = this.createPropertyCard(property);
                cardsContainer.appendChild(card);
            });
            
            container.appendChild(cardsContainer);
        }
    }
    
    createPropertyCard(property) {
        const card = document.createElement('div');
        card.className = 'property-card';
        
        card.innerHTML = `
            <h4>${property.title}</h4>
            <div class="property-price">${property.price}</div>
            <div class="property-details">
                <span>${property.bhk}</span>
                <span>${property.carpet_area}</span>
                <span>${property.status}</span>
            </div>
            <div class="property-location">
                📍 ${property.locality}, ${property.city}
            </div>
            <div class="property-amenities">
                ${property.amenities.map(amenity => 
                    `<span class="amenity-tag">${amenity}</span>`
                ).join('')}
            </div>
            <div class="possession-date">
                🗓️ ${property.possession_date}
            </div>
            <button class="property-cta" onclick="viewProperty('${property.url}')">
                View Details
            </button>
        `;
        
        return card;
    }
    
    addBotResponse(response) {
        this.addMessage(response, 'bot');
    }
    
    setLoading(loading) {
        if (loading) {
            this.sendButton.disabled = true;
            this.sendButton.textContent = 'Sending...';
            this.showTypingIndicator();
        } else {
            this.sendButton.disabled = false;
            this.sendButton.textContent = 'Send';
            this.hideTypingIndicator();
        }
    }
    
    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message';
        typingDiv.id = 'typingIndicator';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content typing-indicator';
        
        contentDiv.innerHTML = `
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        
        typingDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
}

// Global function for CTA
function viewProperty(url) {
    alert(`Would navigate to: ${url}`);
    // In real implementation: window.location.href = url;
}

// Initialize chat when page loads
document.addEventListener('DOMContentLoaded', () => {
    new PropertyChat();
});






































// Frontend JavaScript for Property Search Chatbot

const API_BASE = 'http://localhost:8000/api';

// DOM Elements
const chatInput = document.getElementById('chat-input');
const sendButton = document.getElementById('send-button');
const chatMessages = document.getElementById('chat-messages');
const loadingSpinner = document.getElementById('loading-spinner');
const suggestionsContainer = document.getElementById('suggestions');

// Sample suggestions
const sampleQueries = [
    "2BHK flat in Pune under ₹80L",
    "3BHK ready to move in Mumbai",
    "1BHK in Chembur under ₹1Cr",
    "2BHK under construction in Pune",
    "3BHK luxury apartment in Mumbai"
];

// Initialize suggestions
function initializeSuggestions() {
    suggestionsContainer.innerHTML = '';
    sampleQueries.forEach(query => {
        const button = document.createElement('button');
        button.className = 'suggestion-btn';
        button.textContent = query;
        button.onclick = () => {
            chatInput.value = query;
            handleSendMessage();
        };
        suggestionsContainer.appendChild(button);
    });
}

// Add message to chat
function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    if (typeof content === 'string') {
        messageDiv.innerHTML = `<p>${content}</p>`;
    } else if (typeof content === 'object') {
        // Handle property cards
        if (content.properties && content.properties.length > 0) {
            messageDiv.innerHTML = `
                <div class="response-container">
                    <div class="summary-section">
                        <h4>🏡 Property Search Results</h4>
                        <p class="summary">${content.summary}</p>
                        <div class="filters-applied">
                            <strong>Filters applied:</strong> 
                            ${Object.entries(content.filters_applied || {}).map(([key, value]) => 
                                `${key}: ${value}`
                            ).join(', ')}
                        </div>
                    </div>
                    
                    <div class="properties-grid">
                        ${content.properties.map(property => `
                            <div class="property-card">
                                ${property.image ? `
                                    <div class="property-image">
                                        <img src="${property.image}" alt="${property.title}" onerror="this.style.display='none'">
                                    </div>
                                ` : ''}
                                
                                <div class="property-details">
                                    <h4>${property.title}</h4>
                                    <div class="property-price">${property.price}</div>
                                    <div class="property-location">
                                        📍 ${property.locality}, ${property.city}
                                    </div>
                                    <div class="property-features">
                                        <span class="feature">${property.bhk}</span>
                                        <span class="feature">${property.carpet_area}</span>
                                        <span class="feature">${property.status}</span>
                                    </div>
                                    ${property.amenities && property.amenities.length > 0 ? `
                                        <div class="amenities">
                                            ${property.amenities.slice(0, 2).map(amenity => 
                                                `<span class="amenity">${amenity}</span>`
                                            ).join('')}
                                        </div>
                                    ` : ''}
                                    <div class="possession">
                                        🗓️ ${property.possession_date}
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                    
                    <div class="results-count">
                        Found ${content.total_results} properties matching your criteria
                    </div>
                </div>
            `;
        } else {
            // No properties found
            messageDiv.innerHTML = `
                <div class="response-container">
                    <div class="no-results">
                        <h4>🔍 No Properties Found</h4>
                        <p class="summary">${content.summary}</p>
                        <div class="suggestions">
                            <strong>Try these searches instead:</strong>
                            <ul>
                                <li>Expand your budget range</li>
                                <li>Search in nearby localities</li>
                                <li>Consider different BHK configurations</li>
                                <li>Check under construction properties</li>
                            </ul>
                        </div>
                    </div>
                </div>
            `;
        }
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Show loading indicator
function showLoading() {
    loadingSpinner.style.display = 'block';
    sendButton.disabled = true;
}

// Hide loading indicator
function hideLoading() {
    loadingSpinner.style.display = 'none';
    sendButton.disabled = false;
}

// Handle sending message
async function handleSendMessage() {
    const query = chatInput.value.trim();
    
    if (!query) return;
    
    // Add user message
    addMessage(query, true);
    chatInput.value = '';
    
    // Show loading
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/chat/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Add bot response
        addMessage(data);
        
    } catch (error) {
        console.error('Error:', error);
        addMessage("Sorry, I'm having trouble connecting to the server. Please try again later.");
    } finally {
        hideLoading();
    }
}

// Event listeners
sendButton.addEventListener('click', handleSendMessage);

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSendMessage();
    }
});

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    initializeSuggestions();
    
    // Add welcome message
    setTimeout(() => {
        addMessage("Hello! I'm your property search assistant. I can help you find properties in Pune and Mumbai. Try asking me about 2BHK flats, budget homes, or ready-to-move properties!");
    }, 500);
});