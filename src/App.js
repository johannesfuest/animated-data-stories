import { useState } from 'react';

import './App.css';
import video1 from './videos/story1.mp4';
import video2 from './videos/story2.mp4';
import video3 from './videos/forecast.mp4';
import video4 from './videos/story3.mp4';

import avatar from './res/avatar.svg';
import left from './res/left.svg';
import right from './res/right.svg';
import help from './res/help.svg';

export default function App() {
  const videos = [video1, video2, video3, video4];
  const [videoIndex, setVideoindex] = useState(0)

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
        <span>MorningByte</span>
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
        <div className={"btn" + (videoIndex >= 1 ? '' : ' hide')}>
          <img className="icn" src={left} onClick={prevVideo} />
        </div>
        <div className="btn">
          <a href='https://devpost.com/software/animated-data-stories'>
            <img className="icn " src={help} />
          </a>
        </div>
        <div className={"btn" + (videoIndex < videos.length - 1 ? '' : ' hide')}>
          <img className="icn" src={right} onClick={nextVideo} />
        </div>
      </div>
    </div>
  );
}
