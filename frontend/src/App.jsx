import { useState } from "react";
import "./App.css";
import axios from "axios";

// require(process.env.API_URL);
const filepath =
  "C:/Users/pc/Downloads/Bot-consulting-Assignment/conversational-ai/media/Linux Commands Cheat Sheet.pdf";
const get_api_url = import.meta.env.VITE_API_URL + "/conversation";
const post_api_url = import.meta.env.VITE_API_URL + "/upload_file/";
console.log(post_api_url);
function App() {
  const [data, setData] = useState();
  const fetchData = async () => {
    const response = await axios.get(get_api_url);
    console.log(response.data.message);
  };

  const getSummary = async () => {
    const response = await axios.post(post_api_url);
    console.log(response.data);
  };

  return (
    <div>
      <textarea />
      {/* <input /> */}
      <button
        onClick={() => {
          fetchData();
        }}
      >
        Send
      </button>
      <button onClick={() => getSummary()}>Upload</button>
    </div>
  );
}

export default App;
