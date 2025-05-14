import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom";
import App from "./App";

function Root() {
	const [data, setData] = useState(() => {
		// Retrieve data from localStorage on initialization
		const savedData = localStorage.getItem("appData");
		return savedData ? JSON.parse(savedData) : null;
	});

	useEffect(() => {
		// Save data to localStorage whenever it changes
		if (data) {
			localStorage.setItem("appData", JSON.stringify(data));
		}
	}, [data]);

	return <App data={data} setData={setData} />;
}

ReactDOM.createRoot(document.getElementById("root")).render(
	<React.StrictMode>
		<Root />
	</React.StrictMode>
);