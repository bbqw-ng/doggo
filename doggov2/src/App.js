import { ReactComponent as ProfileIcon } from './icons/user.svg'
import { ReactComponent as CogWheel } from './icons/settings.svg'
import { ReactComponent as LogOut } from './icons/logout.svg'
import { ReactComponent as ListingsImage } from './icons/listings.svg'
import React, { useState, useEffect, useRef } from 'react';

function App() {

    return (
        <Navbar>
            <NavItem icon={<img src="https://www.thesprucepets.com/thmb/A5Rkkt4HDWLAtUOk4gYybcX02mM=/1080x0/filters:no_upscale():strip_icc()/30078352_448703938920062_6275637137232625664_n-5b0de8c443a1030036f9e15e.jpg" />}>

                {/*Dropdown State*/}
                <DropdownMenu/>

            </NavItem>
        </Navbar>
  );
}

//Functional Component
//Return value - JSX (HTML-like syntax in JS)
//"Props" passes data from parent to child; Components pass data to each other using Props
function Navbar(props) {
    return (
        <nav className="navbar">
            <ul className="navbar-nav">
                <div className="navbar-logo">
                    <a href='/home'>DogGo!</a>
                </div>
                {props.children}
            </ul>
        </nav>
    );
}

//Functional Component
//Returns JSX
//Custom prop called "props.icon", our App function (parent) passes data to NavItem (children)
function NavItem(props) {

    //dropdown menu using the useState function
    //useState returns an array of variables open and setOpen
    //open is a boolean value that tells us if the menu is opened
    //setOpen is a function that is used to change the boolean value (false to be closed on default)
    const [open, setOpen] = useState(false);


    //Event handler for clicking outside of menu to close the menu
    //Uses nav-item class for reference area
    let menuArea = useRef();

    useEffect(() => {
        let handler = (e) => {
            if (!menuArea.current.contains(e.target)) {
                setOpen(false);
            }
        };
        document.addEventListener("mousedown", handler);

        return () => {
            document.removeEventListener("mousedown",handler)
        }
    });

    return (
        <li className="nav-item" ref={menuArea}>
            
            { /*when clicked, flip the current boolean value of open*/ }
            <a className="icon-button" onClick={() => setOpen(!open) }>
                { props.icon }
            </a>

            { /*This is what appears only when open = true*/ }
            { open && props.children }

        </li>
        );
}

function DropdownMenu() {

    function DropdownItem(props) {
        return (
            <a className="menu-item">

                <span className="menu-icon">{props.leftIcon}</span>
                { props.children }

            </a>
        );
    }

    return (
        <div className="dropdown">
            <a href="/profile" className="menu-item">
                <DropdownItem leftIcon={<ProfileIcon />}> your profile </DropdownItem>
            </a>
            <a href="/settings" className="menu-item">
            <DropdownItem leftIcon={<CogWheel />}> account settings </DropdownItem>
            </a>
            <a href="/listings" className="menu-item">
                <DropdownItem leftIcon={<ListingsImage />}> your listings </DropdownItem>
            </a>
            <hr></hr>
            <a href="/signout" className="menu-item">
            <DropdownItem leftIcon={<LogOut />}> sign out </DropdownItem>
            </a>
        </div>
    );
}

export default App;
