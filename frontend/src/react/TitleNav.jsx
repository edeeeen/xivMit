// TitleNav.jsx (corrected snippet)
import { Link } from 'react-router-dom';

export default function TitleNav() {
    return (
        <div id="titleNav">
            <div id="pageTitle">
                <Link to="/">Home</Link>
            </div>
            <div id="nav">
                <div className="dropDown"> {/* Corrected: class to className */}
                    <div className="dropHeader">Account</div> {/* Corrected: class to className */}
                    <div className="dropContent"> {/* Corrected: class to className */}
                    </div>
                </div>
            </div>
        </div>
    )
}