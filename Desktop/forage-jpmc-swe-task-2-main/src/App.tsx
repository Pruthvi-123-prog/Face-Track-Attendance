import React, { Component } from 'react';
import DataStreamer, { ServerRespond } from './DataStreamer';
import Graph from './Graph';
import './App.css';

/**
 * State declaration for <App />
 */
interface IState {
  data: ServerRespond[],
  showGraph: boolean,
}

/**
 * The parent element of the react app.
 * It renders title, button and Graph react element.
 */
class App extends Component<{}, IState> {
  // Save interval ID to clear it when needed
  intervalId: NodeJS.Timeout | undefined;

  constructor(props: {}) {
    super(props);

    this.state = {
      // data saves the server responds.
      // We use this state to parse data down to the child element (Graph) as element property
      data: [],
      showGraph: false,
    };
  }

  /**
   * Render Graph react component with state.data parse as property data
   */
  renderGraph() {
    if (this.state.showGraph) {
      return <Graph data={this.state.data} />;
    }
    return null;
  }

  /**
   * Get new data from server and update the state with the new data continuously
   */
  getDataFromServer() {
    // Show the graph when streaming starts
    this.setState({ showGraph: true });

    // Use setInterval to fetch data every 100ms
    this.intervalId = setInterval(() => {
      DataStreamer.getData((serverResponds: ServerRespond[]) => {
        // Update the state by creating a new array of data
        this.setState({ data: serverResponds });
      });
    }, 100);
  }

  // You can add componentWillUnmount to clear the interval when the component is about to unmount
  componentWillUnmount() {
    // Clear the interval to stop requesting data when the component is unmounted
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }

  /**
   * Render the App react component
   */
  render() {
    return (
      <div className="App">
        <header className="App-header">Bank & Merge Co Task 2</header>
        <div className="App-content">
          <button
            className="btn btn-primary Stream-button"
            // When the button is clicked, it starts fetching data continuously
            onClick={() => { this.getDataFromServer(); }}
          >
            Start Streaming Data
          </button>
          <div className="Graph">
            {this.renderGraph()}
          </div>
        </div>
      </div>
    );
  }
}

export default App;
