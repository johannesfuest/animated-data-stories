import { useState, useEffect } from 'react';

import './App.css';
import video1 from './story1.mp4';
import video2 from './story2.mp4';

import avatar from './avatar.svg';
import left from './left.svg';
import right from './right.svg';
import help from './help.svg';

export default function App() {
  const videos = [video1, video2]
  const [videoIndex, setVideoindex] = useState(0)
  
  useEffect(() =>{
    window.scrollTo(0,document.body.scrollHeight);
  }, []);

  function nextVideo() {
    if (videoIndex + 1 < videos.length) {
      setVideoindex(prevIndex => prevIndex + 1);
    }
  }

  function prevVideo() {
    if (videoIndex - 1 >= 0) {
      setVideoindex(videoIndex - 1);
    }
  }

  return (
    <div className="app">
      <div className="header">
        <span>Data Stories</span>
        <div className="btn">
          <img className="icn" src={avatar} />
        </div>
      </div>
      <div className="player">
        <video width="100%" height="100%" autoPlay controls key={videos[videoIndex]}>
          <source src={videos[videoIndex]} type="video/mp4"/>
          Your browser does not support the video tag.
        </video>
      </div>
      <div className="controls">
        <div className="btn">
          <img className="icn" src={left} onClick={prevVideo} />
        </div>
        <div className="btn">
          <a href='https://devpost.com/software/animated-data-stories'>
            <img className="icn " src={help} />
          </a>
        </div>
        <div className="btn">
          <img className="icn" src={right} onClick={nextVideo} />
        </div>
      </div>
    </div>
  );
}
