# VESTI
I was asked to make a simple CLI to manage a imaginary set of garages and cars for an exercise. The starting lists of garages and cars are saved in *state.json*.
## Commands
* `cinfo`<br>
*Shows information about the currently selected car*
* `clear`<br>
*Clears the cli interface*
* `exit`<br>
*Exits the program*
* `ginfo`<br>
*Shows information about the currently selected garage*
* `hand`<br>
*Shows the currently selected car and garage*
* `help [cmd]`<br>
*Displays a help message for a given command, or a list of commands if none is given*
* `list {-c|-g}`<br>
*Lists all cars (-c) or all garages (-g)*
* `park`<br>
*Parks the currently selected car in the currently selected garage*
* `select {-c|-g} {lisenceplate|garageID}`<br>
*Selects either a car by lisenceplate (-c) or a garage by ID (-g)*
* `unpark`<br>
*Unparks the currently selected car from the currently selected garage
