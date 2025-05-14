import React from 'react';

function App({ data, setData }) {
	// Example: Update data and store it in localStorage
	const handleUpdate = (newData) => {
		setData(newData);
	};

	return (
		<div>
			{/* Example usage */}
			<h1>Welcome to FitTrack</h1>
			<p>Stored Data: {data ? JSON.stringify(data) : "No data available"}</p>
			<button onClick={() => handleUpdate({ challenges: "Updated Data" })}>
				Update Data
			</button>
		</div>
	);
}

export default App;