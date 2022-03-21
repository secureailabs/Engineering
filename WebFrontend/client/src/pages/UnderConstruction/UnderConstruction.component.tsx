import React from 'react';
import { Link } from 'react-router-dom';
import { GoTools } from 'react-icons/go'

const MainMenu: React.FC = () => {
  return (
    <div className='underconstruction'>
      <GoTools size='7.5vh'/>
        <div className='underconstruction__text'>This page is under construction.</div>
      <Link to='/dashboard'>Go back to main menu</Link>
    </div>
  );
};

export default MainMenu;
