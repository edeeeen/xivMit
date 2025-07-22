/****************************************************
 *              Create home component               *
 *         Ask api for the encounters and ask       *
 *      Make divs link to /templates/{shorthand}    *
 ****************************************************/

import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom';
import api from '../api';

function Home() {

    const [encountersJSON, setEncountersJSON] = useState({});
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Request data from api, if it fails give an error only in the console
        // ################### TO ADD: SHOW AN ERROR TO THE USER AND CHECK FOR DB ERRORS #####################
        const fetchData = async () => {
            try {
                const response = await api.get('getEncounters');  // request data
                const data = response.data;
                setEncountersJSON(data); //set state variable to the response JSON
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setIsLoading(false);
            }
        }
        fetchData();
    }, []);
    // Wait until data is fetched to load
    // Maybe make prettier for the user
    if (isLoading) {
        console.log("initial rendering, Data not ready yet...");
        return <div> Loading... </div>
    }

    return (
        <div className="home">
            <h2>Choose an Encounter</h2>
            {/*Map encounter json to the tiers*/}
            {Object.keys(encountersJSON).map(tierName => (
                <div key={tierName} className="">

                    {/*Create a title for the tier (Ex: light-heavyweight, asphedelos, etc) */}
                    <h3 className="tierDiv">
                        {tierName}
                    </h3>

                    <div className="encounterDiv">
                        {/*Map the actual fights aspect of the JSON to different divs*/}
                        {encountersJSON[tierName].map((encounter, index) => (
                            
                            // Set the div to be a clickable Link element to link to /templates/{shorthand}
                            <Link to={`templates/${encounter.shorthand}`} key={`${tierName}-${index}`} className="encounter">
                                {/*Display image/check for errors*/}
                                {encounter.imgLink && encounter.imgLink !== "" ? (
                                    <img src={encounter.imgLink} className="encounterImg" />
                                ) : (
                                    // If there is an img error then it will just display the first character of the shorthand
                                    // This is not good something else needs to be done
                                    <div className="imgError">
                                        {encounter.shorthand.charAt(0)}
                                    </div>
                                )}

                                {/*Display shorthand and boss name*/}
                                <div>
                                    <p className="shorthand">
                                        <span className="font-semibold">Shorthand:</span> {encounter.shorthand}
                                    </p>
                                    <p className="bossName">
                                        <span className="font-semibold">Boss:</span> {encounter.boss}
                                    </p>
                                </div>
                            </Link>
                        ))}
                    </div>

                </div>
            ))}
        </div>
    );
}

export default Home;