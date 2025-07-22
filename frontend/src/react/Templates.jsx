/**************************************************
 *  Generate template component based on the URL  *
 *Then request api for user templates and display *
 **************************************************/
import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom';
import api from '../api';

function Templates() {
    const { short } = useParams(); // Get the 'short' parameter from the URL 
    const [templatesJSON, setTemplatesJSON] = useState({});
    const [isLoading, setIsLoading] = useState(true);
    
    useEffect(() => {
        // Request data from api, if it fails give an error only in the console
        // ################### TO ADD: SHOW AN ERROR TO THE USER AND CHECK FOR DB ERRORS #####################
        const fetchData = async () => {
            try {
                const response = await api.get('getTemplates/' + short);  // request data
                const data = response.data;
                //console.log(data);
                setTemplatesJSON(data); //set state variable to the response JSON
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setIsLoading(false);
            }
        }
        fetchData();
    }, []);

    if(isLoading) {
        return (
            <div>Loading...</div>
        );
    }

    return (
        
        <div className="templates">
            <h2>Choose a template</h2>
            <div className="templatesDiv">
                {/*Map the actual fights aspect of the JSON to different divs*/}
                {Object.values(templatesJSON).map((template, index) => (
                    
                    // Set the div to be a clickable Link element to link to /templates/{shorthand}
                    <Link to={`templates/${template.id}`} key={`${template.id}-${index}`} className="template">
                        {/*Display shorthand and boss name*/}
                        <p className="templateName">
                            <span className="font-semibold">Name: {template.name}</span> 
                        </p>
                        <p className="templateBookmarkCount">
                            <span className="font-semibold">Bookmarks: {template.bookmarks}</span> 
                        </p>
                        <p className="templateViewCount">
                            <span className="font-semibold">Name: {template.views}</span> 
                        </p>
                        <p className="templateUsername">
                            <span className="font-semibold">Name: {template.user}</span> 
                        </p>
                        <p className="templateDescription">
                            <span className="font-semibold">Description: {template.description}</span> 
                        </p>

                    </Link>
                ))}
            </div>
        </div>


    );
}

export default Templates;