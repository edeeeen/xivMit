import { useState, useEffect } from 'react'
import './App.css'
import 'react-dom/client';
import { BrowserRouter, Route, Link, Routes } from 'react-router-dom';
import Home from'./react/Home.jsx';
import TitleNav from './react/TitleNav.jsx';
import Templates from './react/Templates.jsx';


function App() {
  const [count, setCount] = useState(0)

  return (
        
        

        

        
    <BrowserRouter>
        <TitleNav></TitleNav>
        <div id="content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/home" element={<Home />} />
              <Route path="/templates/:short" element={<Templates />} />
            </Routes>
             
        </div>


    </BrowserRouter>
        

        
  );
}

export default App
