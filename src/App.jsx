import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Challenges from "./pages/Challenges";
import NotFound from "./pages/NotFound";

function App({ data, setData }) {
	return (
		<Router>
			<Routes>
				<Route path="/" element={<Home />} />
				<Route path="/challenges" element={<Challenges />} />
				<Route path="*" element={<NotFound />} />
			</Routes>
		</Router>
	);
}

export default App;