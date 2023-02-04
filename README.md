# AstraV2
Astra N-body simulation V2

N-BODY V2 CHECKLIST:
1. Finish GUI (Deadline: February 9)
	- Gridline Size adapt with Zoom
		- Not Yet Complete
	- Spawn particles
		- DONE (Jan. 28, 2023)
		- Blink and Glow effect (DONE, February 1, 2023)
	- draw a line indicating direction and velocity of particle launch
		- DONE (Jan. 28, 2023)
	- make particles follow the pan and zoom
		- DONE (Jan. 28, 2023)
	- Overall working UI pan, zoom, spawn
		- 3/4 (gridline scaling needs work)

	- Design the main window + More Customizability + More Interactability
		- buttons
			- Options
				- Window Size Options (Drowpdown)
					- 1080p 16:9 (1920 x 1080)
					- 1024p 5:4 (1280 x 1024)
					- 900p 16:9 (1600 x 900)
					- 720p 16:9 (1280 x 720)
				- Music Volume (Slider)
				- Sound Effects Volume (Slider)

			- Pause and Continue (integrate with "P" shortcut)
				- the buttons switches logos to indicate instead of two separate

			- Speed Up (integrate with timestep "dt" variable)
				- Default Speed Logo (timestep = 0.01)
				- Fast Forward Logo (timestep = 0.05)
				- Fast Fast Forward Logo (timestep = 0.1)
				- the buttons switches logos to indicate instead of two separate

			- Spawn Single Body

			- Spawn Galaxy
				- Switching Galaxy and Single Body
				- the buttons switches logos to indicate instead of two separate

			- Save States and Load States (Integrate with SaveState() and LoadStates() respectively)

		- Customization For
			- Galaxy Spawning (Text Field)
				- Center Mass, Galaxy Size, Galaxy Radius, body masses, body velocity, side angle, side angle speeds are customizable
			- Single Body Spawning (Text Field)
				- Customizable Mass
		- Sounds For
			- Spawning SFX
			- Button Clicking SFX (both for main menu and main simulation)
			- BGM (seperate for Main Menu and Simulation Window)
			
2. Algorithm (Deadline: February 16)
	- make an optimized version of Euler N-body
		- Kinda? Needs some rework i think but not sure at this point (Jan 30, 2023)
		- Galaxy spawning needs some work (there seems to be an extra particle launching from the center and the galaxy is not going to the vector i wanted to) (DONE: Feb. 4 2023)
	- Make the galaxy spawning customizable
	- Create Barnes-Hut Alogrithm
	- Ability to switch between Euler and Barnes-Hut seamlessly
	- Integrate Algorithm with the GUI

3. Main Menu (Deadline: February 20)
	- Design a main menu
	- completed assets
	- working main menu

4. Hardware Accelerated Function (Deadline: Optional)
	- Ability to use GPU whenever available

5. Load and Save Particles
	- fix edge cases (DONE: Feb. 4, 2023)
	- Unfocused window after using file dialog (No current solutions/workarounds except for using other gui)
