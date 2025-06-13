// Templates.jsx (corrected)
import { useParams } from 'react-router-dom'; // Import useParams

export default function Templates() {
    const { short } = useParams(); // Get the 'short' parameter from the URL 
    // short = "test"; // Remove this line unless you specifically need to override
    return (
        <div className="templates">You are looking at {short} templates</div>
    );
}