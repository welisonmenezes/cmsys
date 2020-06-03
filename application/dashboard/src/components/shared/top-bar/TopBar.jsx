import React from "react";
import { IoIosMenu, IoIosArrowRoundBack, IoIosClose } from "react-icons/io";
import "./TopBar.scss";

const TopBar = () => {
    return (
        <div className="TopBar d-flex align-items-center">
            <ul className="d-flex align-items-center menu-icons">
                <li>
                    <span className="btn-icon nice-transition">
                        <IoIosMenu />
                    </span>
                </li>
                <li>
                    <span className="btn-icon nice-transition">
                        <IoIosArrowRoundBack />
                    </span>
                </li>
                <li>
                    <span className="btn-icon nice-transition">
                        <IoIosClose />
                    </span>
                </li>
            </ul>
        </div>
    );
};

export default TopBar;
