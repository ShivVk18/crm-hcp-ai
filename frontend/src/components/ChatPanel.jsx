import React, { useState, useRef, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Bot, User, Send, TriangleAlert } from 'lucide-react';
import { addChatMessage, setInteraction } from '../store';
import { useChatMutation } from '../apiSlice';

const ChatPanel = () => {
  const dispatch = useDispatch();
  const messages = useSelector((state) => state.interaction.chatMessages);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);
  const [sendMessage, { isLoading }] = useChatMutation();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { id: Date.now(), type: 'user', text: input };
    dispatch(addChatMessage(userMessage));
    const currentInput = input;
    setInput('');
    await processMessage(currentInput);
  };

  const handleDisambiguation = async (selectedName, context) => {
    let payload = "";
    if (context.tool === "edit_interaction") {
      payload = `Edit interaction for ${selectedName}. Updates: ${JSON.stringify(context.updates)}`;
    } else if (context.tool === "get_hcp_insights") {
      payload = `Get insights for ${selectedName}`;
    }

    dispatch(addChatMessage({ id: Date.now(), type: 'user', text: `Selected: ${selectedName}` }));
    await processMessage(payload);
  };

  const processMessage = async (textPayload) => {

    try {
      // In a real app, this connects to the backend agent endpoints (/chat or /agent)
      // and receives responses directly powered by LangGraph & Groq
      const response = await sendMessage(textPayload).unwrap();
      
      let botText = "I've logged that interaction.";
      const resData = response.response || response.output || response;

      if (typeof resData === 'string') {
        botText = resData;
      } else if (typeof resData === 'object' && resData !== null) {
        // Automatically populate the form panel with extracted data!
        if (resData.data) {
          dispatch(setInteraction(resData.data));
        }

        if (resData.error) {
          botText = `Error: ${resData.error}`;
        } else if (resData.suggestion) {
          botText = resData.suggestion;
        } else if (resData.summary) {
          botText = resData.summary;
        } else if (resData.message) {
          botText = resData.message;
          if (resData.updated_fields && resData.updated_fields.length > 0) {
            botText += `\nUpdated fields: ${resData.updated_fields.join(', ')}`;
          }
        } else if (resData.doctor !== undefined) {
          botText = `Found ${resData.total_interactions} interactions for ${resData.doctor}.`;
        } else {
          botText = JSON.stringify(resData);
        }
      } else if (response.message) {
        botText = response.message;
      }

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: botText,
        options: resData.options || [],
        context: resData.context || null
      };
      dispatch(addChatMessage(botMessage));
    } catch (error) {
      console.error("Chat error:", error);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: "I couldn't reach the agent backend. Note: Ensure the backend is running and the GROQ_API_KEY is set."
      };
      dispatch(addChatMessage(errorMessage));
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-50 relative">
      <div className="p-4 bg-white border-b border-amber-100 flex items-center gap-2">
        <Bot className="h-5 w-5 text-amber-600" />
        <div>
          <h3 className="font-semibold text-slate-800">AI Assistant</h3>
          <p className="text-xs text-slate-500">Log interaction via chat</p>
        </div>
      </div>

      <div className="flex-1 p-4 overflow-y-auto space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[85%] p-3 rounded-2xl ${
                msg.type === 'user'
                  ? 'bg-amber-600 text-white rounded-br-none'
                  : 'bg-white border border-slate-200 text-slate-700 rounded-bl-none shadow-sm'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.text}</p>
              {msg.options && msg.options.length > 0 && (
                <div className="mt-3 space-y-2">
                  {msg.options.map((opt) => (
                    <button
                      key={opt}
                      onClick={() => handleDisambiguation(opt, msg.context)}
                      className="block w-full text-left px-3 py-2 text-sm font-medium text-amber-700 bg-amber-50 hover:bg-amber-100 rounded-lg transition-colors border border-amber-200"
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border border-slate-200 text-slate-700 p-3 rounded-2xl rounded-bl-none shadow-sm flex items-center gap-2">
              <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></span>
              <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-75"></span>
              <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-150"></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 bg-white border-t border-amber-100">
        <form onSubmit={handleSend} className="relative flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Describe interaction..."
            className="w-full pl-4 pr-12 py-3 border border-slate-300 rounded-full focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none text-sm transition-shadow shadow-sm"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="absolute right-2 p-2 bg-amber-600 hover:bg-amber-700 disabled:bg-slate-300 text-white rounded-full transition-colors"
          >
            <Send className="h-4 w-4" />
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatPanel;
