"use strict";
function Home() {
    const [encountersJSON, setEncountersJSON] = React.useState({});
    const [isLoading, setIsLoading] = React.useState(true);
    // useEffect takes two params. The first param is the function to be run. 
    // The second param is a list of state variables that (if they change) will 
    // cause the function (first param) to be run again.
    // RUN ONCE PATTERN: With [] as 2nd param, it runs the 1st param (fn) just once. 
    
    React.useEffect(async () => {
        const fetchData = async () => {
            try {
                const response = await fetch('api/getEncounters');
                const data = await response.json();
                setEncountersJSON(data);
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                // Ensure isLoading is set to false whether the fetch succeeds or fails
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
        <div class="home">
            <h2>Choose an Encounter</h2>
            {/* Iterate over the keys (tier names) of the encountersJSON object */}
                {Object.keys(encountersJSON).map(tierName => (
                    <div key={tierName} className="">
                        {/* Display the tier name in an h3 tag */}
                        <h3 className="tierDiv">
                            {tierName}
                        </h3>
                        <div className="encounterDiv">
                            {/* Iterate over the array of encounters within each tier */}
                            {encountersJSON[tierName].map((encounter, index) => (
                                <div key={`${tierName}-${index}`} className="">
                                    {/* Display image if imgLink exists and is not empty */}
                                    {encounter.imgLink && encounter.imgLink !== "" ? (
                                        <img src={encounter.imgLink} className="encounterImg"
                                        />
                                    ) : (
                                        // Placeholder circle with shorthand initial if no image
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
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            {/*{
                encountersJSON.map((listObj, index) => 
                    <div>
                        <h3>listObj</h3>
                    </div>
                    
                )
            }
            <div>
                <h1>Cruiserweight</h1>
                <div>m5s</div>
            </div>
            */}
            
        </div>
    );
}