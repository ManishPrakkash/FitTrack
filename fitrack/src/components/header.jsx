import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="flex justify-between items-center p-4 bg-gray-800 text-white">
      <div className="text-lg font-bold">Fitrack</div>
      <nav className="flex items-center space-x-4">
        {/* Circular login/profile button */}
        <Link
          to="/login"
          className="flex items-center justify-center w-10 h-10 bg-primary text-primary-foreground rounded-full hover:bg-primary/90"
          title="Login"
        >
          L
        </Link>
      </nav>
    </header>
  );
};

export default Header;