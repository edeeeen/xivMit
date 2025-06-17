/****************************************************
 *         Generate the titlenav component          *
 ****************************************************/
import { Link } from 'react-router-dom';

function TitleNav() {
    return (
        <div id="titleNav">
            <div id="pageTitle">
                <Link to="/">Home</Link>
            </div>
            <div id="nav">
                <div className="dropDown">
                    <div className="dropHeader">Account</div>
                    <div className="dropContent">
                    </div>
                </div>
            </div>
        </div>
    )
}

export default TitleNav;