/**************************************************
 *  Generate template component based on the URL  *
 *Then request api for user templates and display *
 **************************************************/
import { useParams } from 'react-router-dom';

function Templates() {
    const { short } = useParams(); // Get the 'short' parameter from the URL 
    return (
        <div className="templates">You are looking at {short} templates</div>
    );
}

export default Templates;