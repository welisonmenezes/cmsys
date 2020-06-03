import React from 'react';
import { IoIosMenu, IoIosArrowRoundBack, IoIosClose } from "react-icons/io";
import './TopBar.scss';

function TopBar() {

    return (
        <div className="TopBar d-flex align-items-center">
            <ul className="d-flex align-items-center menu-icons">
                <li>
                    <span className="btn-icon">
                        <IoIosMenu />
                    </span>
                </li>
                <li>
                    <span className="btn-icon">
                        <IoIosArrowRoundBack />
                    </span>
                </li>
                <li>
                    <span className="btn-icon">
                        <IoIosClose />
                    </span>
                </li>
            </ul>
        </div>
    );
}

export default TopBar;
