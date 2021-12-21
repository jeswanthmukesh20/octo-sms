import React, { Component } from 'react';

class App extends Component {
  render() {
    return (
      <div className="App">
        <video id="video" width="640" height="480" autoplay></video>
        <button id="snap">Snap Photo</button>
        <canvas id="canvas" width="640" height="480"></canvas>
      </div>
    );
  }
}



export default App;
