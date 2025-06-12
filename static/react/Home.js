"use strict";
function Home() {
    // useEffect takes two params. The first param is the function to be run. 
    // The second param is a list of state variables that (if they change) will 
    // cause the function (first param) to be run again.
    // RUN ONCE PATTERN: With [] as 2nd param, it runs the 1st param (fn) just once. 
    var encountersJSON
    console.log("UserFilterTable running!!");
    React.useEffect(() => {
        encountersJSON = fetchAPI("encounters");

    }, []);
    
    return (
        <div class="home">
            <h2>Choose an Encounter</h2>
            {
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

            
        </div>
    );
}