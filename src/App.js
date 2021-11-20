import './App.css';
import video1 from './story1.mp4';
import avatar from './avatar.svg';

export default function App() {
  return (
    <div className="app">
      <div className="header">
        <span>Data Stories</span>
        <div className="btn">
          <img className="avatar" src={avatar} />
        </div>
      </div>
      <div className="player">
      <video width="100%" height="100%" autoPlay controls>
          <source src={video1} type="video/mp4"/>
          Your browser does not support the video tag.
        </video>
      </div>
    </div>
  );
}
