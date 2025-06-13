import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'; // Don't forget to import Link if you use it in Home.jsx
import api from '../api'; // Assuming this correctly points to your custom API module

export default function Home() {

    const [encountersJSON, setEncountersJSON] = useState({});
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                // Assuming 'api.get' uses Axios or similar that returns data directly
                const response = await api.get('getEncounters');
                // Access the data via response.data (typical for Axios)
                const data = response.data; // <--- FIX IS HERE

                setEncountersJSON(data);
            } catch (error) {
                console.error('Error fetching data:', error);
                // Consider setting a state to show an error message to the user
            } finally {
                setIsLoading(false);
            }
        }
        fetchData();
    }, []);

    if (isLoading) {
        console.log("initial rendering, Data not ready yet...");
        return <div> Loading... </div>
    }

    return (
        <div className="home">
            <h2>Choose an Encounter</h2>
            {Object.keys(encountersJSON).map(tierName => (
                <div key={tierName} className="">
                    <h3 className="tierDiv">
                        {tierName}
                    </h3>
                    <div className="encounterDiv">
                        {encountersJSON[tierName].map((encounter, index) => (
                            <Link to={`templates/${encounter.shorthand}`} key={`${tierName}-${index}`} className="encounter">
                                {encounter.imgLink && encounter.imgLink !== "" ? (
                                    <img src={encounter.imgLink} className="encounterImg" />
                                ) : (
                                    <div className="imgError">
                                        {encounter.shorthand.charAt(0)}
                                    </div>
                                )}
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