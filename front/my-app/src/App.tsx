import * as React from "react";
import "./App.css";
import Openlayers from "./Openlayers";

class App extends React.Component {
  public render() {
    return (
      <div className="App">
        <p className="App-intro">
          To get started, edit <code>src/App.tsx</code> and save to reload.
        </p>
        <Openlayers />
      </div>
    );
  }
}

export default App;
