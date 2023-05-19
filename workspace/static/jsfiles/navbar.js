function createNavItem(icon, dropdownMenu) {
    const navItem = document.createElement('li');
    navItem.className = 'nav-item';

    const iconButton = document.createElement('a');
    iconButton.className = 'icon-button';

    const iconImage = document.createElement('img');
    iconImage.src = 'https://images.pexels.com/photos/3658120/pexels-photo-3658120.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2';
    iconButton.appendChild(iconImage);

    // Menu doesn't appear initially
    dropdownMenu.style.display = 'none';

    let isOpen = false;

    // Function to toggle the dropdown
    const toggleDropdown = () => {
        isOpen = !isOpen;
        dropdownMenu.style.display = isOpen ? 'block' : 'none';
    };

    // Event listener to toggle the dropdown when clicking on the icon button
    iconButton.addEventListener('click', toggleDropdown);

    // Event listener to close the dropdown when clicking outside of it
    document.addEventListener('click', (event) => {
        if (!navItem.contains(event.target)) {
            isOpen = false;
            dropdownMenu.style.display = 'none';
        }
    });

    navItem.appendChild(iconButton);
    navItem.appendChild(dropdownMenu);

    return navItem;
}

function createDropdownItem(leftIcon, label) {
    const dropdownItem = document.createElement('a');
    dropdownItem.className = 'menu-item';

    const leftIconSpan = document.createElement('span');
    leftIconSpan.className = 'menu-icon';
    leftIconSpan.appendChild(leftIcon);

    dropdownItem.appendChild(leftIconSpan);
    dropdownItem.appendChild(document.createTextNode(label));

    return dropdownItem;
}

function createDropdownMenu() {
    const dropdown = document.createElement('div');
    dropdown.className = 'dropdown';

    const profileLink = document.createElement('a');
    profileLink.href = '/profile';
    profileLink.className = 'menu-item';

    const ProfileIcon = document.createElement('img')
    ProfileIcon.src = 'https://www.pngplay.com/wp-content/uploads/12/User-Avatar-Profile-Transparent-Images-Clip-Art.png';
    ProfileIcon.style.width = 22 + "px";
    const profileItem = createDropdownItem(ProfileIcon, 'your profile');
    profileLink.appendChild(profileItem);
    dropdown.appendChild(profileLink);

  
    const settingsLink = document.createElement('a');
    settingsLink.href = '/settings';
    settingsLink.className = 'menu-item';

    const SettingsIcon = document.createElement('img');
    SettingsIcon.src = 'https://cdn.icon-icons.com/icons2/1875/PNG/512/cog_120288.png';
    SettingsIcon.style.width = 26 + 'px';
    const settingsItem = createDropdownItem(SettingsIcon, 'account settings');
    settingsLink.appendChild(settingsItem);
    dropdown.appendChild(settingsLink);

    const listingsLink = document.createElement('a');
    listingsLink.href = '/listings';
    listingsLink.className = 'menu-item';

    const ListingsIcon = document.createElement('img');
    ListingsIcon.src = 'https://www.iconpacks.net/icons/2/free-search-icon-3076-thumb.png';
    ListingsIcon.style.width = 25 + 'px';
    const listingsItem = createDropdownItem(ListingsIcon, 'your listings');
    listingsLink.appendChild(listingsItem);
    dropdown.appendChild(listingsLink);

    const hr = document.createElement('hr');
    dropdown.appendChild(hr);

    const signOutLink = document.createElement('a');
    signOutLink.href = '/signout';
    signOutLink.className = 'menu-item';

    const SignOutIcon = document.createElement('img');
    SignOutIcon.src = 'https://icons.veryicon.com/png/o/internet--web/website-icons/logout-8.png';
    SignOutIcon.style.width = 20 + 'px';
    const signOutItem = createDropdownItem(SignOutIcon, 'sign out');
    signOutLink.appendChild(signOutItem);
    dropdown.appendChild(signOutLink);

    return dropdown;
}

function createNavbar() {
    const navbar = document.createElement('nav');
    navbar.className = 'navbar';

    const navbarList = document.createElement('ul');
    navbarList.className = 'navbar-nav';

    const navbarLogo = document.createElement('div');
    navbarLogo.className = 'navbar-logo';
    const logoLink = document.createElement('a');
    logoLink.href = '/home';
    logoLink.appendChild(document.createTextNode('DogGo!'));
    navbarLogo.appendChild(logoLink);

    navbarList.appendChild(navbarLogo);
    navbar.appendChild(navbarList);

    const navItem = createNavItem(document.createElement('img'), createDropdownMenu());
    navbarList.appendChild(navItem);

    return navbar;
}

document.addEventListener('DOMContentLoaded', function () {
    const appContainer = document.getElementById('app');
    const navbar = createNavbar();
    appContainer.appendChild(navbar);
});
